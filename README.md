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
In addition to that, a monitoring board is put in place using Telegraf to collect metrics and visualize in Chronograf.
<br/>
![architecture](https://github.com/medaharrat/anomalies-detection/blob/main/docs/Architecture.png)

Each part of the project is containerized using Docker, in addition to two built images

## Technologies
The following technologies are used:

### Kafka
Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.
### PySpark
PySpark is an interface for Apache Spark in Python. It not only allows you to write Spark applications using Python APIs, but also provides the PySpark shell for interactively analyzing your data in a distributed environment. PySpark supports most of Spark’s features such as Spark SQL, DataFrame, Streaming, MLlib (Machine Learning) and Spark Core.
### InfluxDB
InfluxDB is an open-source time series database developed by the company InfluxData. It is written in the Go programming language for storage and retrieval of time series data in fields such as operations monitoring, application metrics, Internet of Things sensor data, and real-time analytics
### Grafana
Grafana is a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources
### Chronograf
Chronograf is an open-source web application and visualization tool developed by InfluxData as part of the InfluxDB project
### Telegraf
Telegraf is a plugin-driven server agent for collecting & reporting metrics. Telegraf has plugins to source a variety of metrics directly from the system it’s running on, pull metrics from third-party APIs, or even listen for metrics via a statsd and Kafka consumer services.

## Run the project
```sh
sh run.sh
```