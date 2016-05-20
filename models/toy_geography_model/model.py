__author__ = 'SEOKHO'

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction import FeatureHasher
import numpy as np

#local file location, change to run
pums = pd.read_csv("C:/CS194/pums/initial_features.csv", delimiter = ',', dtype = 'float')
'''
labels = [label[0] for label in pums.as_matrix(columns = ["PUMA"])]
pums = pums.fillna(0)
raw_features = pums.as_matrix(columns = [column for column in pums.columns if column != "PUMA"])

#features = FeatureHasher(n_features = 5, input_type = 'string', non_negative = True).transform(string_features)
clf = GaussianNB()
clf.fit(raw_features[:1000], labels[:1000])
#this gets us our probability distribution
print(clf.predict_proba(raw_features))
'''
#use metro/micro to predict with household electricity
household = pd.read_csv("../../data/household_electricity_usage/recs2009_public.csv", delimiter = ',', dtype = 'str')
household = household.fillna(0)
raw_features = household.as_matrix(columns = ["DIVISION", ""])
print(raw_features[0])
print("Num Null", np.sum(np.isnan(raw_features)))
raw_features = np.nan_to_num(raw_features)
#features = FeatureHasher(n_features = 5, input_type = 'string', non_negative = True).transform(string_features)

print(clf.predict(raw_features))