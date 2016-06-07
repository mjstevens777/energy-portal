__author__ = 'SEOKHO'

import pandas as pd
import numpy as np

household = pd.read_csv("../household_work_file.csv")

if 'KWH' in household:
    del household['KWH']

kwh_table = pd.read_csv("../../data/household_electricity_usage/recs2009_public.csv")
kwh = np.reshape(kwh_table.as_matrix(columns = ['KWH']), (-1))

print(kwh.shape)
print(household.shape)

household['KWH'] = pd.DataFrame(kwh, columns = ['KWH'])

print(household.shape)
print([column for column in household.columns if 'puma' not in column])

household.to_csv("../household_work_file.csv", index = False)