import os
import boto3
from dotenv import load_dotenv
from scrapy.spiders import Spider

# Load environment variables from .env file
load_dotenv()

class Spider2(Spider):
    name = 'spider2'
    start_urls = ['https://www.softwareadvice.com/categories/']

    def parse(self, response):
        # Extract the entire HTML content of the page
        page_content = response.css('body').get()
        
        # Print the entire HTML content
        print(1, page_content)

        # Write the HTML content to S3 bucket
        s3 = boto3.client('s3',
                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                          region_name=os.getenv('AWS_REGION'))
        bucket_name = 'dinostomach'  
        object_key = 'example1.html'  
        s3.put_object(Body=page_content, Bucket=bucket_name, Key=object_key)
