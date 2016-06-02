__author__ = 'SEOKHO'

import pandas as pd
import numpy as np


pums = pd.read_csv("../pums_ELEP_predicted.csv", delimiter = ',')
left_matrix = pums[['PUMA', 'WGTP', 'SERIALNO']]
del pums['PUMA']
del pums['WGTP']
del pums['SERIALNO']
del pums['ELEP']
pums_puma_vector = pums.as_matrix(columns = ['PUMA'])

for index, val in enumerate(pums_puma_vector):
    if np.isnan(val):
        print(index, val)

'''
household = pd.read_csv("../household_work_file.csv")
print('PUMA' in household.columns)
puma = household.as_matrix(columns = ['PUMA'])
for index, val in enumerate(puma):
    if np.isnan(val):
        print(index, val)
'''
pums = pd.read_csv("../hdd_cdd_interpolation/joined_weather.csv")
pums_puma_vector = pums.as_matrix(columns = ['PUMA'])

for index, val in enumerate(pums_puma_vector):
    if np.isnan(val):
        print(index, val)