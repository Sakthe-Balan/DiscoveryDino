import os
import json
import boto3
from dotenv import load_dotenv
from scrapy import Spider, Request
from math import ceil

# Instructions for integrating with FastAPI
# ----------------------------------------
# 1. Import this spider into your FastAPI application's main.py file.
# 2. Use the Scrapy CrawlerProcess to run the spider.
# 3. Define an endpoint in your FastAPI application that triggers the spider.
# 4. Call the spider using its name ('custom_scraper' in this case) when the endpoint is hit.
# Replace 'YOUR_START_URL_HERE', 'YOUR_CSS_SELECTOR_HERE', 'YOUR_BUCKET_NAME', and 'YOUR_FOLDER_NAME' with actual values.


# Load environment variables from .env file
load_dotenv()

class CustomScraper(Spider):
    name = 'custom_scraper'
    start_urls = ['YOUR_START_URL_HERE'] # Define your start URLs here
    output_file = 'custom_output.json' # Output file name
    bucket_name = 'YOUR_BUCKET_NAME' # S3 bucket name
    folder_name = 'YOUR_FOLDER_NAME' # S3 folder name

    def parse(self, response):
        # Custom parsing logic goes here
        # Example: Extract links from the page
        links = response.css('YOUR_CSS_SELECTOR_HERE').extract()

        for link in links:
            # Customize the request to the extracted links
            yield Request(link, callback=self.custom_parse_method)

    def custom_parse_method(self, response):
        # Custom parsing logic for each extracted link
        # Example: Extract product details
        product_data = {
            'title': response.css('YOUR_CSS_SELECTOR_HERE').get(),
            'description': response.css('YOUR_CSS_SELECTOR_HERE').get(),
            # Add more fields as needed
        }

        # Custom processing or storage logic
        # Example: Save product data to a file or database
        self.save_data(product_data)

    def save_data(self, data):
        # Custom logic to save data
        # Example: Save to a JSON file
        file_exists = os.path.exists(self.output_file) and os.path.getsize(self.output_file) > 0

        with open(self.output_file, 'a') as json_file:
            if not file_exists:
                json_file.write('[') # Add opening square bracket if the file is empty
            else:
                json_file.write(',') # Add comma to separate JSON objects

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


