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
from dino.dino.spiders.spider3 import Spider3
from multiprocessing import Process
from typing import Optional, Dict
from importlib import import_module


from typing import Optional

load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("MONGO_URI")


# Initialize MongoDB client with server API version 1
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

app = FastAPI()

# Global dictionary to store running spider processes
running_spiders: Dict[str, Process] = {}

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
    # Store the process in the global dictionary using the spider class name as the key
    running_spiders[spider_class.__name__] = process
    return process

@app.get("/scrape")
async def scrape_data():
    # Start both spiders in separate processes
    process1 = run_spider(Spider1)
    process2 = run_spider(Spider2)
    process3 = run_spider(Spider3)
    # Wait for both processes to complete
    process1.join()
    process2.join()
    process3.join()
    return {"message": "Scraping completed"}

@app.post("/stop_spider/{spider_name}")
async def stop_spider(spider_name: str):
    """
    Endpoint to stop a running spider.
    
    Parameters:
    spider_name (str): The name of the class of the spider to stop.
    
    Returns:
    dict: A message indicating whether the spider was stopped successfully.
    """
    if spider_name in running_spiders:
        process = running_spiders[spider_name]
        process.terminate()
        process.join() # Wait for the process to terminate
        del running_spiders[spider_name] # Remove the process from the dictionary
        return {"message": f"Spider {spider_name} stopped successfully."}
    else:
        return {"message": f"No spider with the name {spider_name} is currently running."}

@app.get("/run_spider/{spider_name}")
async def run_specific_spider(spider_name: str):
    """
    Endpoint to run a specific spider by name.
    
    Parameters:
    spider_name (str): The name of the class of the spider to be run.
    
    Returns:
    dict: A message indicating whether the spider was started successfully.
    """
    try:
        spider_class = globals().get(spider_name)
        if spider_class and isinstance(spider_class, type):
            run_spider(spider_class)
            return {"message": f"{spider_name} started successfully."}
        else:
            raise HTTPException(status_code=404, detail="Spider not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Run the FastAPI app using Uvicorn server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    
