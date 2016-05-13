__author__ = 'SEOKHO'

from sklearn import cross_validation
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import csv
import numpy as np
from collections import Counter
from sklearn.feature_selection import SelectFromModel

#uses only the household

def loadData(filename, label = "BTUEL", otherRemove = [], forceUse = None):
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
                if forceUse == None or key in forceUse:
                    try:
                        float(row[key])
                    except:
                        if key in allKeys:
                            allKeys.remove(key)
                else:
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
    #allKeys, X, y = loadData("../../data/household_electricity_usage/recs2009_public.csv", label = "BTUEL", otherRemove = [], forceUse =
    #                         [
    #                           'WGTP', 'NP', 'TYPE', 'ACR', 'BDSP', 'BATH', 'FS','MHP', 'RMSP', 'RNTP', 'REFR', 'RNTP', 'RWAT', 'STOV', 'TEN', 'VALP', 'YBL', 'FES', 'FINCP', 'HINCP', 'HHT', 'KIT', 'NOC', 'NPF', 'PLM', 'SRNT', 'SVAL', 'TAXP', 'WIF', 'WORKSTAT',
    #                         ])

    clf = RandomForestRegressor(n_estimators = 100, n_jobs = 7)
    clf.fit(X, y)

    model = SelectFromModel(clf, prefit = True)
    X = model.transform(X)

    relevantFeatures = [allKeys[i] for i in range(len(model._get_support_mask())) if model._get_support_mask()[i] == True]
    print("Relevant Features", relevantFeatures)

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.25)


    clf.fit(X_train, y_train)
    print(y_test[:100])
    print(metrics.mean_squared_error(clf.predict(X_test), y_test))
    features = sorted(zip(allKeys, clf.feature_importances_), key = lambda x : x[1], reverse = True)
    print("Features", features)



if __name__ == "__main__":
    run()