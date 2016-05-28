__author__ = 'SEOKHO'

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.feature_extraction import FeatureHasher
import numpy as np


#local file location, change to run
pums = pd.read_csv("../../join/pums_to_household_norm/join_features_normalized.csv", delimiter = ',')

labels = [label[0] for label in pums.as_matrix(columns = ["PUMA"])]
pums = pums.fillna(0)
raw_features = pums.as_matrix(columns = [column for column in pums.columns if column not in ['PUMA', 'WGTP', 'SERIALNO']])
print(raw_features.shape)
numTrain = 3164116
#numTrain = 10000

#features = FeatureHasher(n_features = 5, input_type = 'string', non_negative = True).transform(string_features)
#clf = RandomForestClassifier(n_estimators = 20)
#clf.fit(raw_features[:1000], labels[:1000])
clf = GaussianNB()
clf.fit(raw_features[:numTrain], labels[:numTrain])
print(clf.classes_)
print(clf.classes_.shape)

#this gets us our probability distribution
prediction = clf.predict_proba([raw_features[0]])
print(prediction.shape)
print(prediction)

print("Model Trained")


household = pd.read_csv("household_normalized_renamed.csv", delimiter = ',')
household = household.fillna(0)
predict_features = household.as_matrix()

print(predict_features.shape)
#features = FeatureHasher(n_features = 5, input_type = 'string', non_negative = True).transform(string_features)

probabilities = clf.predict_proba(predict_features)

print("Predicted", probabilities.shape)
for i, row in enumerate(probabilities):
    for j, val in enumerate(row):
        if val < 1E-5:
            probabilities[i, j] = 0

probabilityFrame = pd.DataFrame(probabilities, columns = ["puma_prob"+str(x) for x in range(probabilities.shape[1])])
print("Tabled")
joined = pd.concat((household, probabilityFrame), axis = 1)
print("Joined")

print(joined.shape)

joined.to_csv("household_wpuma_prob.csv", index = False)