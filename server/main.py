import os
import json
import uvicorn
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks,Query,Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dino.dino.spiders.spider1 import Spider1
from dino.dino.spiders.spider2 import Spider2
from dino.dino.spiders.spider3 import Spider3
from dino.dino.spiders.spider4 import Spider4
from multiprocessing import Process
from typing import Optional, Dict , List , Any
from importlib import import_module


from typing import Optional

load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("MONGO_URI")


# Initialize MongoDB client with server API version 1
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

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
        return {"message": "Welcome to G2 Server v2",
                "DB_Status": "Pinged your deployment. You successfully connected to MongoDB!"}
    except Exception as e:
        return {"message": f"The following exception occurred: {e}", "status": 404}


@app.get("/api/data")
async def get_data(limit: int = Query(..., description="The number of documents to retrieve")):
    """
    Endpoint to retrieve a specified number of documents from a MongoDB collection.
    
    Parameters:
    limit (int): The number of documents to retrieve.
    
    Returns:
    List[Dict[str, Any]]: A list of documents from the specified collection.
    """
    
    try:
        # Assuming 'client' is your MongoClient instance
        db_name = os.getenv("DB_NAME") # Assuming you have a DB_NAME environment variable
        collection_name = "filtered_products" # Assuming you have a COLLECTION_NAME environment variable
        if not db_name or not collection_name:
            raise ValueError("DB_NAME or COLLECTION_NAME environment variable is not set")
        db = client[db_name]
       
        collection = db[collection_name]
        
        documents = collection.find({}).limit(limit)
        # Initialize an empty list to store serialized JSON objects
        # Serialize MongoDB documents to JSON format
        json_documents = [json.loads(json.dumps(doc, default=str)) for doc in documents]
        
        return json_documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

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
    
