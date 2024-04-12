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
import subprocess



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
    
@app.get("/api/search")
async def search_data(collection: str = Query(..., description="Name of the collection to search in"),
                      searchString: str = Query(None, description="String to search for in productName"),
                      limit: int = Query(None, description="The number of documents to retrieve")):
    """
    Endpoint to search for a specific string within a specified collection based on productName.

    Parameters:
    - collection (str): Name of the MongoDB collection to search in.
    - searchString (str): String to search for within the productName field.

    Returns:
    - JSON response containing the search results.
    """
    try:
        # Get the database name from environment variables
        db_name = os.getenv("DB_NAME")
        if not db_name:
            return {"error": "DB_NAME environment variable is not set"}

        # Connect to the specified MongoDB database
        db = client[db_name]

        # Check if the specified collection exists in the database
        if collection not in db.list_collection_names():
            return {"error": f"Collection '{collection}' not found"}

        # Retrieve the specified collection
        target_collection = db[collection]

        # Perform the search query to find documents matching the searchString in productName
        if searchString:
            query = {"productName": {"$regex": f".*{searchString}.*", "$options": "i"}}
        else:
            query = {}
        if limit:
            search_results = list(target_collection.find(query).limit(limit))
        else:
            search_results = list(target_collection.find(query))

        # Convert MongoDB cursor results to JSON format
        # json_results = json.dumps(search_results)
        json_results = [json.loads(json.dumps(doc, default=str)) for doc in search_results]

        return {"collection": collection, "searchString": searchString, "results": json_results}

    except Exception as e:
        return {"error": str(e)}
    
@app.get("/api/filter")
async def filter_data(collection: str = Query(..., description="Name of the collection to search in"),
                      rating: str = Query(None, description="The number of stars to filter from"),
                      category: str = Query(None, description="Pick the category to filter from"),
                      limit: int = Query(None, description="The number of documents to retrieve")
                      ):
    """
    Endpoint to search for a specific string within a specified collection based on productName.

    Parameters:
    - collection (str): Name of the MongoDB collection to search in.
    - searchString (str): String to search for within the productName field.

    Returns:
    - JSON response containing the search results.
    """

    try:
        # Get the database name from environment variables
        db_name = os.getenv("DB_NAME")
        if not db_name:
            return {"error": "DB_NAME environment variable is not set"}

        # Connect to the specified MongoDB database
        db = client[db_name]

        # Check if the specified collection exists in the database
        if collection not in db.list_collection_names():
            return {"error": f"Collection '{collection}' not found"}

        # Retrieve the specified collection
        target_collection = db[collection]

        query = {}

        # Add category filter to the query if category is provided
        if category:
            # query['category'] = category
            query['category'] = {'$in': [category]}

        # Add rating filter to the query if rating is provided and valid
        if rating:
            try:
                rating_num = float(rating)  # Convert rating to a float for numeric comparison
                query['rating'] = {'$gte': rating_num}  # Example: Find documents with rating greater than or equal to 'rating_num'
            except ValueError:
                pass  # Ignore if rating cannot be converted to a float
        if limit:
            search_results = list(target_collection.find(query).limit(limit))
        else:
            search_results = list(target_collection.find(query))

        # Convert MongoDB cursor results to JSON format
        # json_results = json.dumps(search_results)
        json_results = [json.loads(json.dumps(doc, default=str)) for doc in search_results]

        return {"collection": collection, "results": json_results}

    except Exception as e:
        return {"error": str(e)}   
    
    
    pass

@app.get("/preprocess")
def preprocess():
        command = ["pip", "install", "-r", "./preprocess/requirements.txt"]
        subprocess.run(command, check=True)
        subprocess.run(["python", "./preprocess/part1.py"], check=True)
        subprocess.run(["python", "./preprocess/part2.py"], check=True)
def _run_spider(spider_class):
    """
    Internal function to run a Scrapy spider in a CrawlerProcess.
    
    Args:
        spider_class: The class of the spider to run.
    """
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_class)
    process.start()

def run_spider(spider_class):
    """
    Function to run a Scrapy spider in a separate process.
    
    Args:
        spider_class: The class of the spider to run.
        
    Returns:
        process: The process running the spider.
    """
    process = Process(target=_run_spider, args=(spider_class,))
    process.start()
    # Store the process in the global dictionary using the spider class name as the key
    running_spiders[spider_class.__name__] = process
    return process

@app.get("/scrape")
async def scrape_data():
    """
    Endpoint to initiate scraping by starting spiders in separate processes.
    
    Returns:
        JSON response: Message indicating scraping completion.
    """
    # Start spiders in separate processes
    process1 = run_spider(Spider1)
    process2 = run_spider(Spider2)
    process3 = run_spider(Spider3)
    # process4 = run_spider(Spider4)
    
    # Optionally, wait for all processes to complete
    # process1.join()
    # process2.join()
    # process3.join()
    # process4.join()
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
    
