import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import pickle

# Importing the dataset
data = pd.read_csv('./data/SWaT_train.csv', delimiter=',')

# Fit
epsilons = [2, 8, 10, 12]
min_samples = [20, 40, 50, 60]
scores = []

# Tune
for (e, ms) in zip(epsilons, min_samples):
  dbscan = DBSCAN(min_samples = ms, eps = e)
  dbscan.fit( data.iloc[:, data.columns != 'Time'] )
  scores.append(silhouette_score( data.iloc[:, data.columns != 'Time'], dbscan.labels_ ))

# Print results
# print("|#| The best score was: %.3f"%max(scores) + " was achieved by eps: %.2f"%epsilons[scores.index(max(scores))] + " and min_samples: %d"%min_samples[scores.index(max(scores))])

# Fit
db = DBSCAN(min_samples = min_samples[scores.index(max(scores))], eps = epsilons[scores.index(max(scores))])

# Save model
try:
  with open('./models/dbscan.pickle', 'wb') as f:
    pickle.dump(db, f)
except Exception as ex:
  print(f'> {str(ex)}')