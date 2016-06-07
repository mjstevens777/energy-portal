__author__ = 'SEOKHO'

import pandas as pd
import numpy as np

household = pd.read_csv("../household_work_file.csv")
if 'HDD' in household:
    del household['HDD']
    del household['CDD']
if 'HDD30YR' in household:
    del household['HDD30YR']
    del household['CDD30YR']
for column in household.columns:
    if 'Unnamed' in column:
        del household[column]

original_household = pd.read_csv("../../data/household_electricity_usage/recs2009_public.csv")

cdd_hdd = original_household.as_matrix(columns = ['CDD30YR', 'HDD30YR'])
cdd_hdd = np.nan_to_num(cdd_hdd)
cdd_hdd_df = pd.DataFrame(cdd_hdd, columns = ['CDD30YR', 'HDD30YR'])

household['CDD'] = cdd_hdd_df['CDD30YR']
household['HDD'] = cdd_hdd_df['HDD30YR']

print(list(household.shape))
print([column for column in household.columns if 'puma' not in column])

household.to_csv("../household_work_file.csv", index = False)