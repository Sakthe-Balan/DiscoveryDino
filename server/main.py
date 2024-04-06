import os
import uvicorn
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dino.dino.spiders.spider1 import Spider1
from dino.dino.spiders.spider2 import Spider2
from multiprocessing import Process



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
    

def _run_spider(spider_class):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_class)
    process.start()

def run_spider(spider_class):
    process = Process(target=_run_spider, args=(spider_class,))
    process.start()
    return process

@app.get("/scrape")
async def scrape_data():
    # Start both spiders in separate processes
    process1 = run_spider(Spider1)
    # process2 = run_spider(Spider2)

    # Wait for both processes to complete
    process1.join()
    # process2.join()

    return {"message": "Scraping completed"}


# Run the FastAPI app using Uvicorn server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    
