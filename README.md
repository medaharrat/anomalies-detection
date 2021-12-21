# Anomaly Detection in Secure Water Treatment Systems.
## Background
This project serves as an assignment project for the Open Source Technologies / Stream Mining subjects.
## Purpose
The project task is to visualize summaries of the data stream(s) and develop an ML model to detect anomalies in the data set.
## Architecture
The project streams data from an xlsx file through Kafka to a topic called SWAT.
This topic is then subscribed by the PySpark instance in another container.
Each batch is pre-processed and stored in InfluxDB as a data point together with anomalies.
Data is visualized in Grafana in 4 different boards representing anomalies detected using four different approaches.
In addition to that, a monitoring board is put in place using Telegraf to collect metrics.
![architecture](https://github.com/medaharrat/anomalies-detection/blob/main/docs/OST_SM.png)

Each part of the project is containerized using Docker, in addition to two built images