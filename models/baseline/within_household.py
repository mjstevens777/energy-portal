__author__ = 'SEOKHO'

from sklearn import cross_validation
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import csv
import numpy as np
from collections import Counter

#uses only the household

def loadData(filename, label = "USEEL"): #for natgas, label = USENG
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
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            values = []
            for key in row:
                if key in allKeys:
                    values.append(row[key])
            X.append(values)
    return np.asarray(X), np.asarray(y)


def run():
    X, y = loadData("../../data/household_electricity_usage/recs2009_public.csv")
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.25)
    clf = RandomForestRegressor(n_estimators = 100, n_jobs = 7)
    clf.fit(X_train, y_train)
    print(clf.predict(X_test))
    print(Counter(y_test))
    print(metrics.mean_squared_error(clf.predict(X_test), y_test))


if __name__ == "__main__":
    run()