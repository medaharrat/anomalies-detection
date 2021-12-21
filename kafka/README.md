# Kafka
This directory is built as a Docker image (check <a href="https://github.com/medaharrat/anomalies-detection/blob/main/kafka/Dockerfile">Dockerfile</a>) which starts from a python3 base image and runs the producer script.
The script goes through each row of the dataset, produces it to the SWAT topic and stands down for 500ms. This is used to mimic a real-time data stream from streams.
