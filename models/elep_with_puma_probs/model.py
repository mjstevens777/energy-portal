__author__ = 'SEOKHO'

import pandas as pd
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn import cross_validation
from sklearn import metrics
import numpy as np
import json

household = pd.read_csv("../household_complete_distribution.csv")
if 'KWH' in household.columns:
    del household['KWH']

X_columns = [column for column in household.columns if column != "ELEP"]
X = household.as_matrix(columns = X_columns)
y = [label[0] for label in household.as_matrix(columns = ["ELEP"])]

#print(y)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.25)

clf = RandomForestRegressor(n_estimators = 100, n_jobs = 8)
clf.fit(X_train, y_train)


print(y_test[:100])
print(metrics.mean_squared_error(clf.predict(X_test), y_test))
print(metrics.r2_score(y_test, clf.predict(X_test)))

features = sorted(zip(X_columns, clf.feature_importances_), key = lambda x : x[1], reverse = True)
print("Features", features)

#fill spaces in ELEP
normalized_pums = pd.read_csv("../joined_weather.csv", delimiter = ',')
print('pums shape', normalized_pums.shape)

with open("../vectorized_puma_regions/puma_list.json") as f:
    puma_mapping = json.load(f)

reverse_puma_map = {}
for key, value in puma_mapping.items():
    reverse_puma_map[int(value)] = int(key)

pums_puma_vector = normalized_pums.as_matrix(columns = ['PUMA'])

elep_output = []
numPumas = 2378
cache = []
selected_pums = normalized_pums[[column for column in normalized_pums.columns if column not in ['ELEP', 'WGTP', 'SERIALNO', 'PUMA']]]
for index, row in selected_pums.iterrows():
    probs = np.zeros((2378))
    probs[reverse_puma_map[int(pums_puma_vector[index])]] = 1
    other_features = row.as_matrix()
    other_features = np.nan_to_num(other_features)
    X_one_row = np.concatenate((other_features, probs))
    cache.append(X_one_row)
    if len(cache) > 10000:
        elep_output.extend(clf.predict(cache))
        cache = []
    if index % 1000 == 0:
        print(index)
elep_output.extend(clf.predict(cache))

elep_matrix = normalized_pums['ELEP'].as_matrix()

for index, value in enumerate(elep_matrix):
    if not np.isnan(value) and value > 2:
        elep_matrix[index] = value * 12
    else:
        elep_matrix[index] = elep_output[index]

del normalized_pums['ELEP']
normalized_pums['ELEP'] = pd.DataFrame(elep_matrix, columns = ['ELEP'])

normalized_pums.to_csv("../pums_ELEP_predicted.csv", index = False)
