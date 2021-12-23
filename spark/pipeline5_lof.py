#Train LOF on swat_train
# Load packages
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn import preprocessing
from tqdm import tqdm
import pickle

# %matplotlib inline

# Importing the dataset
data = pd.read_csv('./data/SWaT_train.csv', delimiter=',')

# Fit
X = data.iloc[:, data.columns != 'Time']
lof = LocalOutlierFactor(n_neighbors=10).fit(X)

# Save model: It is important to use binary access
with open('./models/lof.pickle', 'wb') as f:
    pickle.dump(lof, f)
