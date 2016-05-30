__author__ = 'SEOKHO'

import pandas as pd
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn import cross_validation
from sklearn import metrics
import numpy as np
import json

kwh_table = pd.read_csv("../../data/household_electricity_usage/recs2009_public.csv", delimiter = ',')
y = kwh_table.as_matrix(columns = ["KWH"])
y = np.reshape(y, (len(y)))

household = pd.read_csv("../pums_geography_model/household_wpuma_prob.csv", delimiter = ',')
X = household.as_matrix()

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.25)

clf = RandomForestRegressor(n_estimators = 10, n_jobs = 8)
clf.fit(X_train, y_train)

kwhOutput = []
pums = pd.read_csv("../pums_ELEP_predicted.csv", delimiter = ',')
pums_puma_vector = pums.as_matrix(columns = ['PUMA'])
left_matrix = pums[['PUMA', 'WGTP', 'SERIALNO']]
del pums['PUMA']
del pums['WGTP']
del pums['SERIALNO']

with open("../vectorized_puma_regions/puma_list.json") as f:
    puma_mapping = json.load(f)

reverse_puma_map = {}
for key, value in puma_mapping.items():
    reverse_puma_map[int(value)] = int(key)

numPumas = 2378
cache = []
for index, row in pums.iterrows():
    probs = np.zeros((2378))
    probs[reverse_puma_map[int(pums_puma_vector[index])]] = 1
    other_features = row.as_matrix()
    other_features = np.nan_to_num(other_features)
    X_one_row = np.concatenate((other_features, probs))
    cache.append(X_one_row)
    if len(cache) > 10000:
        kwhOutput.extend(clf.predict(cache))
        cache = []
    if index % 1000 == 0:
        print(index)
kwhOutput.extend(clf.predict(cache))

print(kwhOutput)

kwhColumn = pd.DataFrame(kwhOutput, columns = ['KWH_MODELED'])

final_table = pd.concat((left_matrix, pums, kwhColumn), axis = 1)

final_table.to_csv("pums_kwh.csv", index = False)

'''
print(y_test[:100])
print(metrics.mean_squared_error(clf.predict(X_test), y_test))

features = sorted(zip(X_columns, clf.feature_importances_), key = lambda x : x[1], reverse = True)
print("Features", features)

#fill spaces in ELEP
normalized_pums = pd.read_csv("C:/CS194/pums/join_features_normalized.csv", delimiter = ',')

for index, row in normalized_pums.iterrows():
    if row['ELEP'] == 2:
        x = row.as_matrix(columns = [column for column in normalized_pums.columns if column not in ['ELEP', 'WGTP', 'SERIALNO', 'PUMA']])
        x = np.nan_to_num(x)
        row['ELEP'] = clf.predict([x])

normalized_pums.to_csv("C:/CS194/pums/pums_ELEP_predicted.csv", index = False)
'''