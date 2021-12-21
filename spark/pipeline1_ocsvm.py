# Train the One Class SVM Model

# Load packages
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.svm import OneClassSVM
from sklearn import preprocessing
from tqdm import tqdm
import pickle

# %matplotlib inline

# Importing the dataset
data = pd.read_csv('./data/SWaT_train.csv', delimiter=',')

# Fit
X = data.iloc[:, data.columns != 'Time']
ocsvm = OneClassSVM(gamma='auto').fit(X)

# Save model: It is important to use binary access
with open('./models/ocsvm.pickle', 'wb') as f:
    pickle.dump(ocsvm, f)