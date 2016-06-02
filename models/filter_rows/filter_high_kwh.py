__author__ = 'SEOKHO'

import pandas as pd

household = pd.read_csv("../household_work_file.csv")
print(household.shape)

to_remove = []
for index, row in household.iterrows():
    if row['KWH'] > 2000:
        to_remove.append(index)

household = household.drop(household.index[to_remove])
print(household.shape)

household.to_csv("../household_work_file.csv", index = False)

