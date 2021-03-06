from pyspark.sql import Row
from sklearn.preprocessing import MinMaxScaler

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import pickle
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime

class InfluxDBWriter:
    def __init__(self, approaches, cloud=False):
        self.url = "http://influxdb:8086"
        self.token = "iJHZR-dq4I5LIpFZCc5bTUHx-I7dyz29ZTO-B4W5DpU4mhPVDFg-aAb2jK4Vz1C6n0DDb6ddA-bJ3EZAanAOUw=="
        self.org = "primary"
        self.bucket = "swat"
        self.approaches = approaches
        if cloud: # Connect to InfluxDB Cloud
            self.client = InfluxDBClient(
                url="<cloud.url>", 
                token="<cloud.token>", 
                org="<cloud.org>"
            )
        else: # Connect to a local instance of InfluxDB
            self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        # Create a writer API
        self.write_api = self.client.write_api()
    
    def _preprocess(self, row):
        # Row to Dict
        row_dict = json.loads(row)
        # Dict to Dataframe
        dataframe = pd.DataFrame(row_dict, index=[0])
        # Rename columns
        cols = list(dataframe.columns)
        cols[1:] = [i.split('_')[1] for i in cols[1:]]
        dataframe.columns = cols
        # Drop unecessary columns
        drop = ['AIT401', 'P102', 'P202', 'P204', 'P206', 'P302',
                'P402','P403','P404','P502','P601','P603', 'Time']
        for col in drop:
            dataframe = dataframe.drop(col, axis=1)
        # Extracct continuous data
        cat = ['MV101','P101','MV201','P201','P203','P205',
            'MV301','MV302','MV303','MV304','P301','P401', 
            'P501','P602','UV401']
        cont = ['FIT101', 'LIT101', 'AIT201', 'AIT202', 'AIT203', 'FIT201',
         'DPIT301',  'FIT301',  'LIT301', 'AIT402', 'FIT401', 'LIT401', 'AIT501', 'AIT502',
         'AIT503',  'AIT504', 'FIT501', 'FIT502',  'FIT503', 'FIT504',  'PIT501',  'PIT502', 
         'PIT503', 'FIT601']

        categ = dataframe[cat]
        continuous = dataframe[cont]
        # PCA and StandardScaler Fitted on train data
        pca = pickle.load(open('./transformers/pca.pickle', 'rb'))
        sc = pickle.load(open('./transformers/scaler.pickle', 'rb'))
        # Normalize
        data_norm = pd.DataFrame( sc.transform(continuous) , columns=continuous.columns)
        # PCA
        reduced = pca.transform( data_norm )
        processed =  pd.DataFrame(data = reduced, columns=[f"P{col + 1}" for col in range(reduced.shape[1])])
        # Merge
        for col in cat:
          processed[col] = dataframe[col]
        return np.asarray(processed)
    
    def process(self, row):
        try:
            self.write_api.write(bucket=self.bucket, org=self.org, record=self._row_to_point(row["data"]))
        except Exception as ex:
            print(f"[x] Error {str(ex)}")

    def _row_to_point(self, row):
        # Load to dictionary
        row_dict = json.loads(row)
        anomaly = 0.0
        points = []
        # String to timestamp
        timestamp = datetime.strptime(row_dict["Time"], "%d/%m/%Y %H:%M:%S.%f %p")
        print(f"> Processing {timestamp}")
        # Handle multiple approaches
        if len(self.approaches) > 1:
            for approach in self.approaches:
                # Create a data point to the approach measurement
                point = Point(approach)
                # Add fields to the point
                row_list = []
                for key, val in row_dict.items():
                    if key != 'Time':
                        point.field(key, float(val))
                        row_list.append(float(val))
                # Predict
                if self._is_anomaly(row, approach)[0] == -1 or (approach == 'kmeans' and self._is_anomaly(row, approach)[0] == 1):
                    point.field('anomaly', np.mean(row_list))
                else:
                    point.field('anomaly', 0.0)
                # Add timestamp
                point.time(timestamp)
                # Append to a list
                points.append(point)
            return points
        else:
            approach = self.approaches[0]
            # Create a data point
            point = Point(approach)
            # Add fields to the point
            row_list = []
            for key, val in row_dict.items():
                if key != 'Time':
                    point.field(key, float(val))
                    row_list.append(float(val))
            # Predict
            if self._is_anomaly(row, approach)[0] == -1 or (approach == 'kmeans' and self._is_anomaly(row, approach)[0] == 1):
                point.field('anomaly', np.mean(row_list))
            else:
                point.field('anomaly', 0.0)
            # Add timestamp
            point.time(timestamp)
        return point
    
    def _is_anomaly(self, row, approach):
        model = ""
        # Import the model
        if approach == 'ocsvm':
            model = "ocsvm.pickle"
        elif approach == 'iso_log':
            model = "iso_log.pickle"
        elif approach == 'kmeans':
            model = "kmeans.pickle"
        elif approach == 'dbscan':
            model = "dbscan.pickle"
        elif approach == 'lof':
            model = "lof.pickle"
        else:
            print(f"[x] {approach} doesn't exist!")

        model = pickle.load(open(f'./models/{model}', 'rb'))
        # Detect anomalies
        preds = None
        if approach == 'lof':
            preds = model.fit_predict(self._preprocess(row).reshape(-1, 1))
        else:
            preds = model.predict(self._preprocess(row))
        return preds

        