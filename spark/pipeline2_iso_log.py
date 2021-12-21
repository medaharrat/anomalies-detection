# Isolation Forest and Logistic Regression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
#%matplotlib inline

def isolotion_tree(data):
    iso=IsolationForest(contamination='auto',random_state=42)
    isol=iso.fit_predict(data)
    return isol

# Load the data
data = pd.read_csv('./data/SWaT_train.csv', delimiter=',')

# Fit Isolation Forest
labels = isolotion_tree(data)

# Logistic Regression
model = LogisticRegression(max_iter=2000)
model.fit(dfc.drop(["Labels"], axis=1), dfc["Labels"])

y_pred=[]   
for x in range(len(sup_data)):
  y_pred.append(model.predict([sup_data.iloc[x]]))

outlier_pos = np.where(y_pred == -1)[0]
x = []; y = [];
for pos in outlier_pos:
    x.append(np.array(sup_data['FIT101'])[pos])
    y.append(sup_data['FIT101'].index[pos])

plt.plot(sup_data["FIT101"].loc[sup_data['FIT101'].index])
plt.plot(y,x,'r*', markersize=5)

