__author__ = 'SEOKHO'

from sklearn import cross_validation
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import csv
import numpy as np
from collections import Counter

#uses only the household

def loadData(filename, label = "BTUEL", otherRemove = []):
    X = []
    y = []
    allKeys = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if len(allKeys) == 0:
                allKeys.extend(row.keys())
            y.append(float(row[label]))
            del row[label]
            for key in row:
                try:
                    float(row[key])
                except:
                    if key in allKeys:
                        allKeys.remove(key)
    allKeys.remove(label)
    for other in otherRemove:
        if other in allKeys:
            allKeys.remove(other)
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            values = []
            for key in row:
                if key in allKeys:
                    values.append(row[key])
            X.append(values)
    return allKeys, np.asarray(X), np.asarray(y)


def run():
    allKeys, X, y = loadData("../../data/household_electricity_usage/recs2009_public.csv", label = "BTUEL", otherRemove =
        ["KWH", "KWHSPH", "KWHCOL", "KWHWTH", "KWHRFG", "KWHOTH", "BTUEL", "BTUELSPH", "BTUELCOL", "BTUELWTH", "BTUELRFG","BTUELOTH",
        "DOLLAREL", "DOLELSPH", "DOLELCOL", "DOLELWTH", "DOLELRFG", "DOLELOTH", "TOTALBTUOTH", "TOTALBTUCOL", 'TOTALBTU', 'TOTALBTUWTH',
         'TOTALBTU', 'TOTALBTUSPH', 'TOTALBTURFG', 'TOTALDOL', 'TOTALDOLSPH', 'TOTALDOLCOL', 'TOTALDOLWTH', 'TOTALDOLRFG', 'TOTALDOLOTH'])
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.25)
    clf = RandomForestRegressor(n_estimators = 100, n_jobs = 7)
    clf.fit(X_train, y_train)
    print(y_test[:100])
    print(metrics.mean_squared_error(clf.predict(X_test), y_test))
    features = sorted(zip(allKeys, clf.feature_importances_), key = lambda x : x[1], reverse = True)
    print(features[:50])



if __name__ == "__main__":
    run()