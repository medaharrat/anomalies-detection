FROM python:3.7
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN mkdir data
COPY ../Data/* /data/
ADD _.py /
CMD ["python" , "_.py"]