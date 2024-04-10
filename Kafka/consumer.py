from confluent_kafka import Consumer, KafkaError
import boto3
import os
import json
import uuid
import time
# Kafka consumer configuration
conf = {'bootstrap.servers': "13.233.130.112:9092", 'group.id': 'spider-consumer'}
consumer = Consumer(conf)

# Subscribe to topic
consumer.subscribe(['softwareadvice'])

# Initialize S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                  region_name=os.getenv('AWS_REGION'))

# Specify the S3 bucket and folder
bucket_name = 'dinostomach'
folder_name = 'kafka'

# Consume messages
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            time.sleep(1)
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                
        
        # Get message value (assuming it's a JSON string)
        message_value = msg.value().decode('utf-8')
        print(f"Received message: {message_value}")

        # Parse JSON string into a dictionary
        json_data = json.loads(message_value)
        
        # Generate a unique file name (UUID)
        file_name = f"{uuid.uuid4()}.json"
        
        # Put the JSON data into a file and upload it to S3
        s3.put_object(Bucket=bucket_name, Key=f"{folder_name}/{file_name}", Body=json.dumps(json_data))
        print(f"Message saved to S3: {file_name}")
except KeyboardInterrupt:
    pass
finally:
    # Close consumer
    consumer.close()
