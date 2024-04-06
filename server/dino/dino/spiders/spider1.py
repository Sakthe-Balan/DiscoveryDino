import os
import json
import boto3
from dotenv import load_dotenv
from scrapy import Spider, Request

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

        products = []

        for card in product_cards:
            # Extract data from each product card
            product_data = {
                'title': card.css('h3::text').get(),
                'description': card.css('p::text').get(),
                'price': card.css('strong::text').get(),
                'image_url': card.css('img::attr(src)').get()
            }

            # Append product data to the list
            products.append(product_data)

        # Save product data to a JSON file
        with open(self.output_file, 'a') as json_file:
            json.dump(products, json_file, indent=4)

        self.logger.info(f'Product data appended to {self.output_file}')

    def closed(self, reason):
        # Upload the JSON file to S3 after the spider is closed
        s3 = boto3.client('s3',
                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                          region_name=os.getenv('AWS_REGION'))

        s3.upload_file(self.output_file, self.bucket_name, f'{self.folder_name}/{self.output_file}')
        self.logger.info(f'{self.output_file} uploaded to {self.bucket_name}/{self.folder_name}/{self.output_file}')
