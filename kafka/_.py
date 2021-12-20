from kafka import KafkaProducer
import json
import csv
import sys
import os 
import time

if __name__ == "__main__":
    BOOTSTRAP_SERVER = 'kafka:9092'
    TOPIC = 'SWAT'
    DATA_PATH = './data/test.csv'
    # Load the data
    print('Loading data')
    data = csv.DictReader(open(DATA_PATH)) 
    # Initialize producer
    producer = KafkaProducer(bootstrap_servers = BOOTSTRAP_SERVER)
    # Time interval
    startTime = time.time()
    waitSeconds = .1

    while True:
        for row in data:
            # Convert to a JSON format
            payload = json.dumps(row)
            # Produce
            producer.send(TOPIC, value=payload.encode('utf-8'))
            # Wait a number of second until next message
            time.sleep(waitSeconds - ((time.time() - startTime) % waitSeconds))
