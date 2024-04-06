import scrapy

class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['http://example.com']

    def parse(self, response):
        # Example: Extracting data from the page
        data = response.css('div.example-class').getall()
        yield {'data': data}
