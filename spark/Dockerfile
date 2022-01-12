FROM jupyter/pyspark-notebook
COPY . .
RUN python3 -m pip install -r requirements.txt
USER root
RUN chmod +x spark-submit.sh

RUN echo '[...] Preprocessing data'
RUN python3 preprocess.py

RUN echo '[...] Fitting models'
RUN python3 pipeline1_ocsvm.py 
RUN python3 pipeline2_iso_log.py 
RUN python3 pipeline3_kmeans.py 
RUN python3 pipeline4_dbscan.py 

RUN echo '[...] Deploy Spark'
ENTRYPOINT ["sh", "./spark-submit.sh"]