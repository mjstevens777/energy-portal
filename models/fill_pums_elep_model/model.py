__author__ = 'SEOKHO'

import pandas as pd
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn import cross_validation
from sklearn import metrics
import numpy as np

kwh_table = pd.read_csv("../../data/household_electricity_usage/recs2009_public.csv", delimiter = ',')
y = kwh_table.as_matrix(columns = ["KWH"])
y = np.reshape(y, (len(y)))

household = pd.read_csv("../pums_geography_model/household_wpuma_prob.csv", delimiter = ',')
X = household.as_matrix()

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.25)

clf = RandomForestRegressor(n_estimators = 10, n_jobs = 8)
clf.fit(X_train, y_train)

kwhOutput = []
pums = pd.read_csv("../../join/pums_to_household_norm/join_features_normalized.csv", delimiter = ',')

for row in pums.iterrows():


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