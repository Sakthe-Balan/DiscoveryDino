import os
import json
import boto3
from dotenv import load_dotenv
from scrapy import Spider, Request
from math import ceil
import uuid
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
            link='https://crozdesk.com'+link
            yield Request(link, callback=self.custom_parse_method)

    def custom_parse_method(self, response):
        # Initialize an empty dictionary to hold all the data
        section=response.css('div.cus_provider-panel')
        for s in section:
            product_data = {
                'title': section.css('span.inline-block::text').get(),
                'image_url': section.css('img::attr(data-src)').get(),
                'view_profile_link': section.css('a.cus_viewprofilelink::attr(href)').get(),
                'reviews': [], # Placeholder for reviews
                'description': [] # Placeholder for description
            }
            print(product_data)
        # Yield a request to extract reviews and description, passing the product_data dictionary
        yield Request('https://crozdesk.com'+product_data['view_profile_link'], callback=self.parse_reviews_and_description, meta={'product_data': product_data})

    def parse_reviews_and_description(self, response):
        # Extracting reviews
        reviews = response.css('div.cus_no-reviews::text').getall()

        # Extracting description
        description = [p.css('::text').get() for p in response.css('#provider_description p')]

        # Update the product_data dictionary with the extracted reviews and description
        product_data = response.meta['product_data']
        product_data['reviews'] = reviews
        product_data['description'] = description
        print(product_data)
        # Yield the final product_data dictionary
        yield product_data

     

    
 # this function executes at the end of the spidder process
    def closed(self, reason):
        
        try:
            s3 = boto3.client('s3',
                            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                            region_name=os.getenv('AWS_REGION'))


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

