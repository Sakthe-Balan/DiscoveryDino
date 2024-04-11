import os
import json
import boto3
from dotenv import load_dotenv
from scrapy import Spider, Request
from math import ceil
import uuid
from confluent_kafka import Producer
import time

# Load environment variables from .env file
load_dotenv()
conf = {'bootstrap.servers':os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        'client.id': 'spider-producer'}
producer = Producer(conf)
class Spider1(Spider):
    name = 'spider1'
    start_urls = ['https://www.softwareadvice.com/categories/']
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


        # Convert product_data to a JSON string
        json_str = json.dumps(product_data)

        # Send the JSON string to the Kafka topic
        producer.produce(self.folder_name, value=json_str.encode('utf-8'))
        producer.flush()  # Ensure the message is delivered
        print(product_data)
        print("Message sent")
       
        


# this function executes at the end of the spidder process
    def closed(self, reason):
        
        producer.flush()
        producer.close()
        try:
            s3 = boto3.client('s3',
                            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                            region_name=os.getenv('AWS_REGION'))

            # Ensure logs.txt exists and is updated regardless of the reason for closure
            logs_file = f'{self.folder_name}/logs.txt'

            try:
                # Attempt to download the current content of logs.txt
                response = s3.get_object(Bucket=self.bucket_name, Key=logs_file)
                current_logs = response['Body'].read()
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
