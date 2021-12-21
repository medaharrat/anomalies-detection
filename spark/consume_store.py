from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

from influx_writer import InfluxDBWriter
from influxdb_client import InfluxDBClient

import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime

if __name__=="__main__":
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'

    # Spark Instance
    spark = SparkSession.builder.master('local[*]').getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')

    # Define an input stream
    cols = ['Time',
    'HMI_FIT101', 'HMI_LIT101', 'HMI_AIT201', 'HMI_AIT202', 'HMI_AIT203', 'HMI_FIT201',
    'HMI_DPIT301', 'HMI_FIT301', 'HMI_LIT301', 'HMI_AIT401', 'HMI_AIT402', 'HMI_FIT401', 
    'HMI_LIT401', 'HMI_AIT501', 'HMI_AIT502', 'HMI_AIT503', 'HMI_AIT504', 'HMI_FIT501',
    'HMI_FIT502', 'HMI_FIT503', 'HMI_FIT504', 'HMI_PIT501', 'HMI_PIT502', 'HMI_PIT503', 
    'HMI_FIT601', 'HMI_MV101', 'HMI_P101', 'HMI_P102', 'HMI_MV201', 'HMI_P201', 'HMI_P202',
    'HMI_P203', 'HMI_P204', 'HMI_P205', 'HMI_P206','HMI_MV301', 'HMI_MV302', 'HMI_MV303',
    'HMI_MV304', 'HMI_P301', 'HMI_P302', 'HMI_P401', 'HMI_P402', 'HMI_P403', 'HMI_P404',
    'HMI_P501', 'HMI_P502', 'HMI_P601', 'HMI_P602', 'HMI_P603', 'HMI_UV401']

    fields = [StructField(col_name, StringType(), True) for col_name in cols]
    schema = StructType(fields)

    # Read stream from json and fit schema
    inputStream = spark\
        .readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "SWAT")\
        .load()

    inputStream = inputStream.select(col("value").cast("string").alias("data"))
    inputStream.printSchema()

    # Delete previous row
    client = InfluxDBClient(url="http://influxdb:8086", token="iJHZR-dq4I5LIpFZCc5bTUHx-I7dyz29ZTO-B4W5DpU4mhPVDFg-aAb2jK4Vz1C6n0DDb6ddA-bJ3EZAanAOUw==", org="primary")
    delete_api = client.delete_api()
    start = "2010-01-01T00:00:00Z"
    measurement = "data"
    delete_api.delete(start, datetime.now(), f'_measurement="{measurement}"', bucket="swat", org="primary")
    print("> Deleted")

    # Read stream and process
    print(f"> Reading the stream and storing ...")
    query = (inputStream
            .writeStream
            .outputMode("append")
            .foreach(InfluxDBWriter( sys.argv[1] ))
            .start())

    query.awaitTermination()