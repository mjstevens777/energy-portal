__author__ = 'SEOKHO'

import pandas as pd

cdd_hdd = pd.read_csv("cdd_hdd.csv")
pums = pd.read_csv("../join_features_normalized.csv")

cdd_mapping = {}
hdd_mapping = {}
for _, row in cdd_hdd.iterrows():
    cdd_mapping[row['PUMA']] = row['CDD']
    hdd_mapping[row['PUMA']] = row['HDD']

cdd = []
hdd = []
for _, row in pums.iterrows():
    cdd.append(cdd_mapping[row['PUMA']])
    hdd.append(hdd_mapping[row['PUMA']])

join = pd.concat((pums, pd.DataFrame(cdd, columns = ["CDD"]), pd.DataFrame(hdd, columns = ["HDD"])), axis = 1)

#join.drop(join.columns[-3], axis=1)
print(join.columns)
print(join.columns.shape)

join.to_csv("joined_weather.csv", index = False)