FROM jupyter/pyspark-notebook
COPY . .
RUN python3 -m pip install -r requirements.txt
USER root
RUN chmod +x spark-submit.sh

RUN echo '[...] Deploy Spark'
ENTRYPOINT ["sh", "./spark-submit.sh"]