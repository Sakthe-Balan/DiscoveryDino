import os
import json
import boto3
import scrapy
from dotenv import load_dotenv
from scrapy import Request
from math import ceil
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()
links=['/all']
class Spider3(scrapy.Spider):
    name = 'spider3'
    start_urls = ['https://www.producthunt.com/']
    output_file = 'final.json'
    bucket_name = 'dinostomach'
    folder_name = 'producthunt'

    def parse(self, response):
        # Start date
        start_date = datetime(2024, 1, 1)
        # End date
        end_date = datetime(2019, 1, 1)

        # Loop through each date, decreasing from start_date to end_date
        current_date = start_date
        while current_date >= end_date:
            # Construct the date part of the URL
            date_part = current_date.strftime("%Y/%m/%d")
            # Construct the URL
            url = f'https://www.producthunt.com/leaderboard/daily/{date_part}/all'
            # Make a request to the URL with custom_parse_method callback
            yield Request(url, callback=self.custom_parse_method)
            # Decrease the date by one day
            current_date -= timedelta(days=1)

    def custom_parse_method(self, response):
        # Loop through each div with the specified class name
          for div in response.css('div.styles_item__Dk_nz.my-2.flex.flex-1.flex-row.gap-2.py-2.sm\:gap-4'):
            # Extracting title
            title = div.css('strong::text').get()
            print(title)
            # Extracting image_url
            image_url = div.css('img.styles_mediaThumbnail__NCzNO::attr(src)').get()
            print(image_url)
            # Extracting website
            website = 'https://www.producthunt.com/' + div.css('a.styles_externalLinkIcon__vjPDi::attr(href)').get()
            print(website)
            # Create mets
            mets = {'title': title, 'image_url': image_url, 'website': website}
            titles =title.lower(). replace(" ", "-")
           
            # Request the detailed page
            detailed_url = 'https://www.producthunt.com/' + f'posts/{titles}'
            mets['link'] = detailed_url
            print(detailed_url)
            links.extend(response.css('a.text-14.font-semibold.text-light-grey::attr(href)').extract())
            yield Request(detailed_url, callback=self.parse_detailed_page, meta=mets)

    def parse_detailed_page(self, response):
        mets = response.meta
        # Extracting description
        description = response.css('div.styles_htmlText__eYPgj.text-16.font-normal.text-dark-grey::text').get()
        if(description == "null" or description == None or description ==""):
            description = response.css('div.text-16.font-normal.text-light-grey.mb-6::text').get()
        
            
        mets['description'] = description
        print(description)
       
        reviews_url = response.url + '/reviews'
        
        yield Request(reviews_url, callback=self.parse_reviews, meta=mets)

    def parse_reviews(self, response):
        mets = response.meta
        reviews = response.css('div.text-18.font-normal.text-dark-grey.text-center.mt-4::text').get()
         # Check if reviews is None or an empty string
        if reviews is None or reviews == "":
        # # Try a different selector
            reviews = response.css('div.styles_htmlText__eYPgj.text-18.font-normal.text-light-grey.italic.styles_format__8NeQe.styles_overallExperience__x7Gqf::text').get()
        
    # If reviews is still None or an empty string, set it to "No reviews" or any other suitable default value
        if reviews is None or reviews == "":
            reviews = "No reviews"
        print(reviews)
    # Add reviews to meta
        mets['reviews'] = [reviews]
        meta_data = {
        'title': mets['title'],
        'image_url': mets['image_url'],
        'website': mets['website'],
        'link': mets['link'],
        'description': mets['description'],
        'reviews': mets['reviews']
    }
        self.save_data(meta_data)

    def save_data(self, data):
        file_exists = os.path.exists(self.output_file) and os.path.getsize(self.output_file) > 0

        with open(self.output_file, 'a') as json_file:
            if not file_exists:
                json_file.write('[')
            else:
                json_file.write(',')

            json.dump(data, json_file, indent=4)


    def closed(self, reason):
        # Custom logic to execute after the spider is closed
        # Example: Upload the JSON file to S3
        with open(self.output_file, 'a') as json_file:
            json_file.write(']') # Add closing square bracket to indicate the end of JSON array

        s3 = boto3.client('s3',
                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                          region_name=os.getenv('AWS_REGION'))

        if os.path.exists(self.output_file) and os.path.getsize(self.output_file) > 0:
            with open(self.output_file, 'r') as json_file:
                existing_data = json.load(json_file)

            total_items = len(existing_data)
            chunk_size = 1000
            num_chunks = ceil(total_items / chunk_size)

            for i in range(num_chunks):
                chunk = existing_data[i * chunk_size: (i + 1) * chunk_size]
                chunk_file = f'custom_output_chunk_{i + 1}.json'
                
                with open(chunk_file, 'w') as chunk_json_file:
                    json.dump(chunk, chunk_json_file, indent=4)
                
                s3.upload_file(chunk_file, self.bucket_name, f'{self.folder_name}/{chunk_file}')
                self.logger.info(f'{chunk_file} uploaded to {self.bucket_name}/{self.folder_name}/{chunk_file}')

                os.remove(chunk_file)



