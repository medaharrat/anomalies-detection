FROM python:3.7
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN mkdir data
ADD ./data/* /data/
ADD _.py /
CMD ["python" , "_.py"]