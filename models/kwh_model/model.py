__author__ = 'SEOKHO'

import pandas as pd
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn import cross_validation
from sklearn import metrics
from sklearn.svm import SVR
from sklearn import svm
import numpy as np
import pickle
import json

household = pd.read_csv("../household_complete_one_hot.csv", delimiter = ',')
y = household.as_matrix(columns = ['KWH'])
y = np.reshape(y, (-1))
y = np.log(y)
del household['KWH']
del household['ELEP']


def select_column(column):
    if 'puma_prob' in column:
        return False
    return True
    #return column in ['BDSP', 'RMSP', 'HFL', 'BLD', 'AGEP', 'NP', 'YBL', 'HINCP', 'HDD', 'CDD']

household = household[[column for column in household.columns if select_column(column)]]
X = household.as_matrix()
print(household.columns)
#X = household.as_matrix()

with open("kwh_model_features.json", "w") as f:
    json.dump(list(household.columns), f, indent = True)

print(y)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.25)

clf = RandomForestRegressor(n_estimators = 50, n_jobs = 8)
clf.fit(X_train, y_train)

print(y_test[:100])
print(np.sqrt(metrics.mean_squared_error(y_test, clf.predict(X_test))))
print(metrics.r2_score(y_test, clf.predict(X_test)))


features = sorted(zip(household.columns, clf.feature_importances_), key = lambda x : x[1], reverse = True)
print("Features", features)


with open("kwh_model.pkl", 'wb') as f:
    pickle.dump(clf, f)
