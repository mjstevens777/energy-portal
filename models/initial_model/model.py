__author__ = 'SEOKHO'

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction import FeatureHasher

metro = pd.read_csv("../../data/metro_micropolitan/processed.csv", delimiter = ',', dtype = 'str')