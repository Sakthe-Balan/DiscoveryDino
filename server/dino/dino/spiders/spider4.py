import os
import json
import boto3
from dotenv import load_dotenv
from scrapy import Spider, Request
from math import ceil

# Load environment variables from .env file
load_dotenv()

class Spider4(Spider):
    name = 'spider4'
    start_urls = ['https://crozdesk.com/browse'] # Define your start URLs here
    output_file = 'custom_output.json' # Output file name
    bucket_name = 'dinostomach' # S3 bucket name
    folder_name = 'crozdesk' # S3 folder name

    def parse(self, response):
        # Custom parsing logic goes here
        # Example: Extract links from the page
        links = response.css('a::attr(href)').extract()
        print(links)
        for link in links:
            # Customize the request to the extracted links
            yield Request(link, callback=self.custom_parse_method)

    def custom_parse_method(self, response):
        # Custom parsing logic for each extracted link
        # Example: Extract product details
        product_data = {
            'title': response.css('.p::text').get(),
            'description': response.css('.div::text').get(),
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
                    chunk_file = f'products_chunk_{i + 1}.json'
                    
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
            if not s3.head_object(Bucket=self.bucket_name, Key=logs_file):
                s3.put_object(Bucket=self.bucket_name, Key=logs_file, Body='')
            else:
                # Download the current content of logs.txt
                s3.download_file(self.bucket_name, logs_file, 'temp_logs.txt')
                with open('temp_logs.txt', 'r') as temp_logs_file:
                    current_logs = temp_logs_file.read()

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

