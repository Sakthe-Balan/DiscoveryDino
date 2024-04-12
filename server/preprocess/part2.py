# h3llo
# %%
import os
import re
import json
import time
import logging
import requests
from tqdm import tqdm 
from rich import print
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import boto3
load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("MONGO_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
G2_API_KEY = os.getenv("G2_API_KEY")

# Configure logging
logging.basicConfig(filename='processing_software_advice.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

s3 = boto3.client('s3',
                            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                            region_name=os.getenv('AWS_REGION'))
bucket_name = 'dinostomach'
folder_name = 'softwareadvice'
object_name = f'{folder_name}/products.json'
    
    # Get the object from S3
response = s3.get_object(Bucket=bucket_name, Key=object_name)
    
    # Read the contents of the object (assuming it's a JSON file)
file_content = response['Body']

# %%
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
chat = ChatOpenAI(temperature=0 , openai_api_key=OPENAI_API_KEY)

# Define the mapping from original keys to new keys
key_mapping = {
    'title': 'productName',
    'description': 'description',
    'price': 'rating',
    'image_url': 'photoUrl',
    'link': 'scarpedLink',
    'additional_info': 'additionalInfo',
    'website': 'website',
    'reviews': 'reviews'
}
# Initialize MongoDB client with server API version 1
category_list = ["Sales Tools", "Marketing", "Analytics Tools & Software", "Artificial Intelligence", "AR/VR", "B2B Marketplaces", "Business Services", "CAD & PLM", "Collaboration & Productivity", "Commerce", "Content Management", "Converged Infrastructure", "Customer Service", "Data Privacy", "Design", "Development", "Digital Advertising Tech", "Ecosystem Service Providers", "ERP", "Governance, Risk & Compliance", "Greentech", "Hosting", "HR", "IoT Management", "IT Infrastructure", "IT Management", "Marketing Services", "Marketplace Apps", "Office", "Other Services", "Professional Services", "Routers", "Security"]

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["g2"]


data = json.load(file_content)

print(len(data))

# %%
def get_categories(transformed_data):
    
    if transformed_data['productName'] and transformed_data['description']:
        
        messages = [
            SystemMessage(
                content="You are an expert at identifying which software belongs to which categories"
            ),
            HumanMessage(
                content=f"""
                Given the following product : {transformed_data['productName']}
                and the product description : {transformed_data['description']}
                and the following categories to pick from : {category_list}
                
                which category does the product belong to
                
                Only respond with a list of categories the product belongs to
                """
            ),
        ]

        response_content=chat.invoke(messages).content
        pattern = r"\['(.*?)'\]"
        categories_match = re.findall(pattern, response_content)
        categories_list = categories_match[0].split("', '") if categories_match else []
        # only return those which are there in category_list
        if len(categories_list) != 0:
                    # Filter categories to only include those present in category_list
            filtered_categories = [cat for cat in categories_list if cat in category_list]

            if filtered_categories:
                return filtered_categories
            # return categories_list
        else:
            logging.error("no category picks from the LLM")
            return []
    else:
        logging.error("error occurse while generating category list")
        return []

def get_mode(transformed_data):
    mode_list = ["B2B" , "B2C"]
    
    if transformed_data['productName'] and transformed_data['description']:
        
        messages = [
            SystemMessage(
                content="You are an expert at identifying which software belongs to which type of business model"
            ),
            HumanMessage(
                content=f"""
                Given the following product : {transformed_data['productName']}
                and the product description : {transformed_data['description']}
                and the following categories to pick from : {mode_list}
                
                which model does the product belong to
                
                Only respond with a list of categories the product belongs to
                
                such as  ['B2B'] or ['B2C'] or ['B2B','B2C'] pick one
                """
            ),
        ]

        response_content=chat.invoke(messages).content
        pattern = r"\['(.*?)'\]"
        categories_match = re.findall(pattern, response_content)
        models_list = categories_match[0].split("', '") if categories_match else []
        # only return those which are there in category_list
        if len(models_list) != 0:
                    # Filter categories to only include those present in category_list
            # filtered_categories = [cat for cat in models_list if cat in mode_list]
            return models_list
            # if filtered_categories:
            #     return filtered_categories
            # return categories_list
        else:
            logging.error("no category picks from the LLM")
            return []
    else:
        logging.error("error occurse while generating category list")
        return []

def write_description(transformed_data):
    
    if transformed_data['productName'] and transformed_data['description'] and transformed_data['additionalInfo']:
        
        messages = [
            SystemMessage(
                content="You are an expert at software products"
            ),
            HumanMessage(
                content=f"""
                referring to this description of the software product {transformed_data['description']} and {transformed_data['additionalInfo']}
                write a detailed description about it possible for customers to understand what it is about the software product not more than 150 words
                """
            ),
        ]
        response_content=chat.invoke(messages).content
        return response_content

def g2_product_search(transformed_data):
    """
    Return True if the product is there in G2 and insert it into MongoDB if not already present.
    """

    url = f"https://data.g2.com/api/v1/products?filter[name]={transformed_data['productName']}"
    headers = {
        'Authorization': f'Bearer {G2_API_KEY}',
    }

    try:
        # Make API request to G2
        response = requests.get(url, headers=headers)
        response_data = response.json()

        # Check if there are any records matching the product name
        record_count = response_data["meta"]["record_count"]
        if record_count > 0:
            # Iterate over the returned data
            for g2_product in response_data["data"]:
                # Check if the product with the same "id" already exists in MongoDB
                existing_product = db['g2_products'].find_one({"id": g2_product["id"]})

                if not existing_product:
                    # Insert the transformed data into the MongoDB collection
                    g2_product["associatedProductName"] = transformed_data['productName']
                    db['g2_products'].insert_one(g2_product)
                    # print("Inserted product with id:", g2_product["id"])

            return True
        else:
            return False

    except requests.RequestException as e:
        logging.error("Error making API request:", e)
        return False

# %%

def process_data(original_data):
    transformed_data = {}
    for original_key, new_key in key_mapping.items():
        if original_key in original_data:
            transformed_data[new_key] = original_data[original_key]
            
    # Add additional fields to the transformed data
    transformed_data['similarProducts'] = []  # List of URLs (empty for now)
    transformed_data['contactMail'] = None  # Contact email (replace with actual email)
    transformed_data['reviews'] = [{'content': review['content']} for review in transformed_data['reviews']]  # Adjust reviews format    
    # Convert the transformed data to JSON
    # Attempt to get categories; retry on failure
    while True:
        try:
            transformed_data['category'] = get_categories(transformed_data)  # List of categories (replace with actual categories)
            break  # Break out of the loop if successful
        except Exception as e:
            logging.error(f"Error getting categories: {e}")
            logging.info("Retrying to get categories...")
            time.sleep(3)  # Wait for 1 second before retrying
    
    # Log processing details to the file
    product_name = transformed_data.get('productName', 'Unknown Product')
    description = transformed_data.get('description', 'No description')
    categories = transformed_data.get('category', [])


    if g2_product_search(transformed_data):
        collection = db['scraped_products_1'] 
        insert_result = collection.insert_one(transformed_data)
        log_message = f"Processing Product: {product_name} | Description: {description} | Categories: {categories} | In G2: {True}"
    else:
        # print("shortlisted")
        while True:
            try:
                transformed_data['business_models'] = get_mode(transformed_data)  # List of categories (replace with actual categories)
                break  # Break out of the loop if successful
            except Exception as e:
                logging.error(f"Error getting categories: {e}")
                logging.info("Retrying to get categories...")
                time.sleep(3)  # Wait for 1 second before retrying
    
        # transformed_data["additionalInfo"] = write_description(transformed_data)
        logging.info(f"Product '{product_name}' not found in G2")
        collection = db['scraped_products_1'] 
        insert_result = collection.insert_one(transformed_data)
        collection = db['filtered_products_1']  
        insert_result = collection.insert_one(transformed_data)
        log_message = f"Processing Product: {product_name} | Description: {description} | Categories: {categories} | In G2: {False}"
    logging.info(log_message)
    # print(transformed_data)

# %%
# #Process individual data from each product
# original_data = data[2]
# print(original_data)
# process_data(original_data)

for product_data in tqdm(data[3500:10000], desc="Processing Products", unit="products"):
    process_data(product_data)

# %%
# print(data[:10])

# %%
# """Code to delete everything in the database"""

# collection_names = ['scraped_products', 'filtered_products', 'g2_products']

# # Loop through each collection and delete all documents
# for collection_name in collection_names:
#     collection = db[collection_name]
#     result = collection.delete_many({})  # Delete all documents in the collection
#     print(f"Deleted {result.deleted_count} documents from '{collection_name}' collection")


# %%
# from pymongo import MongoClient

# # List of collection names to process
# collection_names = ['scraped_products', 'filtered_products', 'g2_products']

# def convert_rating_to_float(collection_name):
#     collection = db[collection_name]

#     # Iterate over each document in the collection
#     for document in collection.find():
#         # Check if the document contains a 'rating' field
#         if 'rating' in document:
#             try:
#                 # Convert 'rating' from string to float
#                 if document["rating"] == None:
#                     rating_float = float(-1)
#                 else:
#                     rating_float = float(document['rating'])
                
#                 # Update the document with the converted rating
#                 collection.update_one(
#                     {'_id': document['_id']},
#                     {'$set': {'rating': rating_float}}
#                 )
#             except ValueError:
#                 # Handle conversion error if 'rating' is not a valid float
#                 print(f"Error converting rating to float for document {_id} in {collection_name}")

# # Process each collection
# for collection_name in collection_names:
#     convert_rating_to_float(collection_name)

# # Close the MongoDB client connection
# # client.close()

