__author__ = 'SEOKHO'

import pandas as pd

#transforms column names
household = pd.read_csv("household_normalized.csv", delimiter = ',')
rename = pd.read_csv("rename.tsv", delimiter = '\t')

print(household.columns)

mapping = {}
for _, row in rename.iterrows():
    mapping[row['household']] = row['pums']

for index, name in enumerate(household.columns.values):
    household.columns.values[index] = mapping[name]

household.to_csv("household_normalized_renamed.csv", index = False)
print(household.columns)