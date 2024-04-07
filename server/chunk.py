import os
import json
import boto3
from math import ceil
import uuid
from dotenv import load_dotenv

load_dotenv()

output_file = 'products.json'
bucket_name = 'dinostomach'  # Update with your AWS S3 bucket name
folder_name = 'getapp'  # Update with your desired folder name in S3
chunk_size = 1000

# Load existing data from the output_file
if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
    with open(output_file, 'r') as json_file:
        existing_data = json.load(json_file)

    total_items = len(existing_data)
    num_chunks = ceil(total_items / chunk_size)

    s3 = boto3.client('s3',
                      aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                      region_name=os.getenv('AWS_REGION'))

    for i in range(num_chunks):
        chunk = existing_data[i * chunk_size: (i + 1) * chunk_size]
        new_uuid = uuid.uuid4()
        chunk_file = f'products_chunk_{new_uuid}.json'

        # Save chunk to a separate JSON file
        with open(chunk_file, 'w') as chunk_json_file:
            json.dump(chunk, chunk_json_file, indent=4)

        # Upload the chunk file to S3
        s3.upload_file(chunk_file, bucket_name, f'{folder_name}/{chunk_file}')

        # Remove the chunk file
        os.remove(chunk_file)
