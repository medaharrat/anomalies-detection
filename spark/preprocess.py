# Data Preprocessing of SWaT Dataset
import os, time, datetime, io, csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Importing the datase
def load_data(path):
  return pd.read_excel(path, header = 1)

# Rewrite column names
def rewrite_cols(data):
  cols = list(data.columns)
  cols[1:] = [(i.split(":"))[2].split(".")[1].split('_')[1] for i in cols[1:]]
  data.columns = cols
  return data

# Data Exploration
def EDA(data):
  ## Data shape
  print(f'[>] Data shape is {data.shape}')
  ## Data types
  print(f'[>] Data types are: ')
  print(data.dtypes)
  ## Missing values 
  print(f'[>] Missing values: ')
  print(data.isnull().sum().sum())
  ## Duplicated rows
  print(f'[>] Duplicated values: ')
  print(data.duplicated().sum())
  ## Values to datetime
  print(f'[...] Converting string time to timestamp')
  data['Time'] = [datetime.datetime.strptime(t, "%d/%m/%Y %H:%M:%S.%f %p") for t in data['Time']] 
  ## Distribution by days
  print(f'[>] Distribution by days: ')
  day = data['Time'].dt.day
  cnt_srs = day.value_counts()
  plt.figure(figsize=(12,6))
  sns.barplot(cnt_srs.index, cnt_srs.values, alpha=0.8, color=sns.color_palette()[3])
  plt.xticks(rotation='vertical')
  plt.xlabel('Date', fontsize=12)
  plt.ylabel('Number of Occurrences', fontsize=12)
  plt.show()
  ## Distribution by hours
  print(f'[>] Distribution by hours: ')
  hours = data['Time'].dt.hour
  cnt_srs = hours.value_counts()
  plt.figure(figsize=(12,6))
  sns.barplot(cnt_srs.index, cnt_srs.values, alpha=0.8, color=sns.color_palette()[3])
  plt.xticks(rotation='vertical')
  plt.xlabel('Hour', fontsize=12)
  plt.ylabel('Number of Occurrences', fontsize=12)
  plt.show()
  ## Plots
  print(f'[>] Plot columns by timestamp: ')
  j = 1
  while j < len(cols)/2:
    plt.figure(figsize = (15, 10))
    for i, col in enumerate(cols[j:j+3]):
      plt.subplot(2, 3, i + 1)    
      plt.scatter(data['Time'], data[col], s=10)
      plt.xlabel('Time')
      plt.title(str(col))
      plt.xticks(rotation=40)
      j += 1
    plt.show()

# Preprocess data
def preprocess(data):
  # Find columns with only one values. We will drop them since they don't have any effect.
  for col in data.columns:
    if len(data[col].value_counts()) == 1:
      print(f"> Dropping {col}")
      data = data.drop(col, axis=1)
  # Get categorical columns
  CATEG_RANGE = 3
  cat, cont = [], []

  for col in data.columns:
    if len(data[col].value_counts()) <= CATEG_RANGE:
      cat.append(col)
    else:
      cont.append(col)

  return data, cat, cont

# Standardize values
def Standardize(data):
  sc = StandardScaler()
  sc.fit(data.iloc[:, data.columns != 'Time'])
  data_norm = pd.DataFrame( sc.transform(data.iloc[:, data.columns != 'Time']) )
  data_norm_c = data_norm.copy()
  data_norm.columns = data.iloc[:, data.columns != 'Time'].columns
  data_norm.insert(0, 'Time', data['Time'])
  # It is important to use binary access
  with open('./transformers/scaler.pickle', 'wb') as f:
    pickle.dump(sc, f)
  return data_norm

# Principal Component Analysis
def apply_pca(data, cont):
  data_scaled = Standardize(data[cont])
  data_ = data_scaled
  pca = PCA(n_components = 0.95)
  pca.fit(data_.iloc[:, data_.columns != 'Time'])
  reduced = pca.transform(data_.iloc[:, data_.columns != 'Time'])
  principal_components = pd.DataFrame(data = reduced, columns=[f"P{col + 1}" for col in range(reduced.shape[1])])
  with open('./transformers/pca.pickle', 'wb') as f:
      pickle.dump(pca, f)
  return principal_components

# Merge extracted features with scaled data
def append_cols(A, B, cols):
  for col in cat:
    A[col] = B[col]
  A.insert(0, 'Time', B['Time'])
  return A

def split_save(data):
  # Split the data
  i = round(len(data)*.8)
  train = data[0:i] # 80% of the data
  test = data[i+1:len(data)] # 20% of the data
  print(len(train), len(test))

  # Split the data into two sets and save locally
  train.to_csv(f"./data/SWaT_train.csv", sep = ',', encoding = 'utf-8', index = False)
  test.to_csv(f"./data/SWaT_test.csv", sep = ',', encoding = 'utf-8', index = False)

if __name__=="__main__":
  # Load data
  LOCAL_PATH = './data/All.xlsx'
  data = load_data(LOCAL_PATH)
  # Rewrite cols
  data = rewrite_cols(data)
  # EDA
  # EDA(data)
  # Preprocess
  data, cat, cont = preprocess(data)
  # PCA
  data_processed = apply_pca(data, cont)
  # Merge
  R = append_cols(data_processed, data, cat)
  # Split and save the data
  split_save(R)