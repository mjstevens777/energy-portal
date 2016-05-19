__author__ = 'SEOKHO'

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction import FeatureHasher

metro = pd.read_csv("../../data/metro_micropolitan/processed.csv", delimiter = ',', dtype = 'str')

labels = [label[0] for label in metro.as_matrix(columns = ["FIPS"])]
string_features = metro.as_matrix(columns = ["MetroMicro"])
features = FeatureHasher(n_features = 5, input_type = 'string', non_negative = True).transform(string_features)
clf = MultinomialNB()
clf.fit(features, labels)
#this gets us our probability distribution
print(clf.predict_proba(features))

#use metro/micro to predict with household electricity
household = pd.read_csv("../../data/household_electricity_usage/recs2009_public.csv", delimiter = ',', dtype = 'str')
string_features = household.as_matrix(columns = ["METROMICRO"])
features = FeatureHasher(n_features = 5, input_type = 'string', non_negative = True).transform(string_features)

print(clf.predict(features))