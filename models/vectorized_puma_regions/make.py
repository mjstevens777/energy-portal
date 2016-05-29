__author__ = 'SEOKHO'

import pandas as pd
import json

pums = pd.read_csv("../../join/pums_to_household_norm/join_features_normalized.csv", delimiter = ',')

mapping = {}

for index, val in enumerate(sorted(list(set(pums['PUMA'])))):
    mapping[index] = str(val)

with open("puma_list.json", "w") as f:
    json.dump(mapping, f, indent = True)