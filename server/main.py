import os
import json
import uvicorn
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI, UploadFile, File, HTTPException
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dino.dino.spiders.my_spider import MySpider
from typing import Optional

load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("MONGO_URI")

# Initialize MongoDB client with server API version 1
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

app = FastAPI()

# Default endpoint
@app.get("/")
async def base_function():
    """
    Default endpoint providing basic information about the service.
    
    Returns:
    dict: A welcome message and database status.
    """
    try:
        # Ping MongoDB to check connection status
        client.admin.command('ping')
        return {"message": "Welcome to G2 Server",
                "DB_Status": "Pinged your deployment. You successfully connected to MongoDB!"}
    except Exception as e:
        return {"message": f"The following exception occurred: {e}", "status": 404}
    
@app.get("/scrape")
def run_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(MySpider)
    process.start() # This will block until the crawling is finished
    return {"message": "Scraping completed"}
    
# Run the FastAPI app using Uvicorn server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
