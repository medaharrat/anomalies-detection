# Spark Streaming
This directory contains the stream processing part of the project.
Data stread is read from a kafka topic and then split into batches. Each batch is processed and stored in InfluxDB.
We are using PySpark for the streaming and InfluxDB as a time series database.

This repo is built as a Docker image (check <a href="https://github.com/medaharrat/anomalies-detection/blob/main/spark/Dockerfile">Dockerfile</a>); It starts with a <a href="https://hub.docker.com/r/jupyter/pyspark-notebook">jupyter-notebook/pyspark</a> image and runs the different stages of the application.