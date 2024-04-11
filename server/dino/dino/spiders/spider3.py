import os
import json
import boto3
import scrapy
from dotenv import load_dotenv
from scrapy import Request
from math import ceil
from datetime import datetime, timedelta
import uuid
from confluent_kafka import Producer
import time

# Load environment variables from .env file
load_dotenv()
conf = {'bootstrap.servers':os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        'client.id': 'spider-producer-2'}
producer = Producer(conf)
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
        # Convert product_data to a JSON string
        json_str = json.dumps(meta_data)

        # Send the JSON string to the Kafka topic
        producer.produce(self.folder_name, value=json_str.encode('utf-8'))
        producer.flush()  # Ensure the message is delivered
        print(meta_data)
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


