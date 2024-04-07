import os
import boto3
from dotenv import load_dotenv
from scrapy import Request
from scrapy.spiders import Spider

# Load environment variables from .env file
load_dotenv()

class Spider2(Spider):
    name = 'spider2'
    start_urls = ['https://www.getapp.com/browse/']

    def parse(self, response):
        # Extracting all links from the base page
        all_links = response.xpath('//a/@href').getall()
        
        # Process each link
        for link in all_links:
            # Scrape data from each page starting from page 1
            page_num = 1
            while True:
                page_link = f"{link.rstrip('/')}/page-{page_num}/"
                yield Request(page_link, callback=self.parse_page)
                
                # Check if any scraped fields are empty
                if self.is_empty_field_obtained(response):
                    break  # Move to the next link if any field is empty
                
                page_num += 1

    def is_empty_field_obtained(self, response):
        # Example logic to check if any scraped fields are empty
        # You can modify this based on your specific fields and conditions
        # Here, we assume that if any field is empty, we return True
        fields_to_check = response.xpath('//your/field/xpath/here').getall()
        return any(field.strip() == '' for field in fields_to_check)

    def parse_page(self, response):
        # Example of parsing data from individual pages
        # Add your parsing logic here
        pass
