from kafka import KafkaProducer
import time
import csv
import binascii
import json

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
    break
