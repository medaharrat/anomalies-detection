from kafka import KafkaProducer
import json
import csv
import sys
import os 
import time

#producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: v.encode('utf-8'))
producer = KafkaProducer(bootstrap_servers='localhost:9092',key_serializer=lambda v: v.encode('utf-8'), value_serializer=lambda v: json.dumps(v).encode('utf-8'))
def sendRowData(data,key,topic):
    producer.send(topic, data, key)
    
csvfile = open('C:/SWAT.csv', 'r')
reader = csv.DictReader(csvfile,fieldnames)
next(reader)
for row in reader:    
    print(row)
    #print(row['id'])
    print(json.dumps(row))
    print(json.dumps(row).encode('utf-8'))
    #print(type(json.dumps(row).encode('utf-8')))
    break
