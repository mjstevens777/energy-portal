__author__ = 'SEOKHO'

import pandas as pd

cdd_hdd = pd.read_csv("cdd_hdd.csv")
pums = pd.read_csv("../join_features_normalized.csv")

pd.concat((pums, cdd_hdd), axis = 1).to_csv("joined_weather.csv")