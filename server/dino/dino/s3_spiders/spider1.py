import os
import json
import boto3
from dotenv import load_dotenv
from scrapy import Spider, Request
from math import ceil
import uuid

# Load environment variables from .env file
load_dotenv()

class Spider1(Spider):
    name = 'spider1'
    start_urls = ['https://www.softwareadvice.com/categories/']
    output_file = 'products.json'
    bucket_name = 'dinostomach'
    folder_name = 'softwareadvice'

    def parse(self, response):
        # Extract links from the page
        links = response.css('a::attr(href)').extract()

        for link in links:
            # Append '/p/all' to the link
            link += '/p/all'

            # Make a request to the category URL
            yield Request(link, callback=self.parse_category)

    def parse_category(self, response):
        # Extract product cards from the category page
        product_cards = response.css('.ProductCardComponent.alternatives-card.mb-4.rounded-lg.border.border-solid.border-grey-100.shadow')

        for card in product_cards:
            # Extract data from each product card
            product_data = {
                'title': card.css('h3::text').get(),
                'description': card.css('p::text').get(),
                'price': card.css('strong::text').get(),
                'image_url': "",
                'link': card.css('a::attr(href)').get()  # Store the link
            }

            # Request to the product link
            yield Request(product_data['link'], callback=self.parse_product_details, meta={'product_data': product_data})

    def parse_product_details(self, response):
        # Retrieve product data from meta
        product_data = response.meta.get('product_data')
        product_data['image_url'] = response.css('img::attr(data-src)').getall()[0]
        # Extract the desired additional information from the div without any class attribute
        additional_info = response.css('div:not([class])::text').get()

        # Add additional info to product data
        product_data['additional_info'] = additional_info.strip() if additional_info else None

        # Request to the review page
        product_data['website'] = response.css('a::attr(data-href)').get()

        review_link = product_data['link'] + '/reviews/'
        yield Request(review_link, callback=self.parse_reviews, meta={'product_data': product_data})

    def parse_reviews(self, response):
        product_data = response.meta.get('product_data')

        # Extracting review divs
        review_divs = response.css('.col-span-12.lg\:col-span-9.lg\:row-span-3.lg\:row-start-2.lg\:pl-8')
        reviews = []

        # Iterate over review divs and scrape the first 3 reviews
        for review_div in review_divs[:3]:
            review = {
                
                'content': review_div.css('p::text').get()
            }
            reviews.append(review)

        # Adding reviews to product_data
        product_data['reviews'] = reviews
        
        file_exists = os.path.exists(self.output_file) and os.path.getsize(self.output_file) > 0

        # Append product data to the JSON file
        with open(self.output_file, 'a') as json_file:
            if not file_exists:
                json_file.write('[')  # Add opening square bracket if the file is empty
            else:
                json_file.write(',')  # Add comma to separate JSON objects

            json.dump(product_data, json_file, indent=4)
        yield product_data



    def closed(self, reason):
        try:
            # Upload the JSON file to S3 after the spider is closed
            with open(self.output_file, 'a') as json_file:
                json_file.write(']') # Add closing square bracket to indicate the end of JSON array
            s3 = boto3.client('s3',
                            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                            region_name=os.getenv('AWS_REGION'))

            # Load existing data from JSON file if it exists and is not empty
            if os.path.exists(self.output_file) and os.path.getsize(self.output_file) > 0:
                with open(self.output_file, 'r') as json_file:
                    existing_data = json.load(json_file)

                total_items = len(existing_data)
                chunk_size = 1000
                num_chunks = ceil(total_items / chunk_size)

                for i in range(num_chunks):
                    chunk = existing_data[i * chunk_size: (i + 1) * chunk_size]
                    unique_id = uuid.uuid4()
                    chunk_file = f'products_chunk_{unique_id}.json'
                    
                    # Save chunk to a separate JSON file
                    with open(chunk_file, 'w') as chunk_json_file:
                        json.dump(chunk, chunk_json_file, indent=4)
                    
                    # Upload the chunk file to S3
                    s3.upload_file(chunk_file, self.bucket_name, f'{self.folder_name}/{chunk_file}')
                    self.logger.info(f'{chunk_file} uploaded to {self.bucket_name}/{self.folder_name}/{chunk_file}')

                    # Remove the chunk file
                    os.remove(chunk_file)

            # Ensure logs.txt exists and is updated regardless of the reason for closure
            logs_file = f'{self.folder_name}/logs.txt'

            try:
                # Attempt to download the current content of logs.txt
                response = s3.get_object(Bucket=self.bucket_name, Key=logs_file)
                current_logs = response['Body'].read().decode('utf-8')
            except s3.exceptions.NoSuchKey:
                # If the logs.txt doesn't exist, create it with an empty content
                current_logs = ""

            # Log success or error message based on the reason
            if reason == 'finished':
                log_message = f"{self.name} finished successfully.\n"
            else:
                log_message = f"{self.name} closed with reason: {reason}\n"

            # Append the new log message to the current logs
            updated_logs = current_logs + log_message

            # Upload the updated logs back to S3
            s3.put_object(Bucket=self.bucket_name, Key=logs_file, Body=updated_logs, ContentType='text/plain', ACL='public-read')
        except Exception as e:
            # Log the error to logs.txt
            error_message = f"Error in {self.name}: {str(e)}\n"
            s3.put_object(Bucket=self.bucket_name, Key=logs_file, Body=error_message, ContentType='text/plain', ACL='public-read')
            self.logger.error(f"Error in {self.name}: {str(e)}")
