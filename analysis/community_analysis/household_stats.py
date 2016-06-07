__author__ = 'SEOKHO'

import pandas as pd
import numpy as np

#household = pd.read_csv("../../data/household_electricity_usage/recs2009_public.csv")
#pums = pd.read_csv("../../join/pums_to_household_norm/join_features.csv")
household = pd.read_csv("../../models/household_complete_distribution.csv")
pums = pd.read_csv("../../models/pums_ELEP_predicted.csv")
'''
print(np.histogram(household['ST']))
print(np.histogram(pums["ST"]))

print(np.histogram(household['DIVISION']))
print(np.histogram(pums['DIVISION']))
'''
print(np.histogram(household['ELEP'], bins = 100))
elep = pums['ELEP'].as_matrix()
print(np.histogram(elep))