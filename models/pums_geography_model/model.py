__author__ = 'SEOKHO'

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.feature_extraction import FeatureHasher
from sklearn import cross_validation
from sklearn import metrics
import numpy as np


def indicator(column, num_values):
    column = column.astype('int')
    matrix = np.zeros((column.shape[0], len(num_values) + 1))
    matrix[np.arange(len(column)), column - column.min()] = 1
    return matrix

def featurize(df):
    full_matrix = None
    for column in df:
        if column == 'BLD':
            sub_matrix = indicator(df[column], np.arange(0, 10))
        else:
            sub_matrix = df[column].as_matrix().reshape((-1, 1))
        if full_matrix == None:
            full_matrix = sub_matrix
        else:
            full_matrix = np.hstack((full_matrix, sub_matrix))
    return full_matrix


#local file location, change to run
pums = pd.read_csv("../../join/pums_to_household_norm/join_features_normalized.csv", delimiter = ',')

#ELEP is a target leak
#del pums["ELEP"]

labels = [label[0] for label in pums.as_matrix(columns = ["PUMA"])]
weights = np.array([weight[0] for weight in pums.as_matrix(columns = ["WGTP"])])
pums = pums.fillna(0)
#pums_feature_table = pums[]
del pums['PUMA']
del pums['WGTP']
del pums['SERIALNO']
raw_features = featurize(pums)
print(raw_features.shape)

X_train, X_test, y_train, y_test, W_train, W_test= cross_validation.train_test_split(raw_features, labels, weights, test_size = 0.01)
numTrain = 3164116
#numTrain = 10000

#features = FeatureHasher(n_features = 5, input_type = 'string', non_negative = True).transform(string_features)
#clf = RandomForestClassifier(n_estimators = 20)
#clf.fit(raw_features[:1000], labels[:1000])
clf = GaussianNB()
clf.fit(X_train, y_train, W_train)

print("LogLoss", metrics.log_loss(y_test, clf.predict_proba(X_test)))

print("Model Trained")


household = pd.read_csv("../../join/pums_to_household_norm/household_normalized_renamed.csv", delimiter = ',')
household = household.fillna(0)

#del household['ELEP']
predict_features = featurize(household)

print(predict_features.shape)
#features = FeatureHasher(n_features = 5, input_type = 'string', non_negative = True).transform(string_features)

probabilities = clf.predict_proba(predict_features)

print("Predicted", probabilities.shape)
'''
for i, row in enumerate(probabilities):
    for j, val in enumerate(row):
        if val < 1E-5:
            probabilities[i, j] = 0
'''
#one hot vector instead
for i, row in enumerate(probabilities):
    probabilities[i, np.argmax(row)] = 1
    for j, val in enumerate(row):
        if val < 1:
            probabilities[i, j] = 0

probabilityFrame = pd.DataFrame(probabilities, columns = ["puma_prob"+str(x) for x in range(probabilities.shape[1])])
print("Tabled")
joined = pd.concat((household, probabilityFrame), axis = 1)
print("Joined")

print(joined.shape)

joined.to_csv("../household_wsingle.csv", index = False)