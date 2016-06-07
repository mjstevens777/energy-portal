__author__ = 'SEOKHO'

import pandas as pd
import numpy as np

#household = pd.read_csv("../../models/household_complete_distribution.csv")
#pums = pd.read_csv("../../models/pums_ELEP_predicted.csv")
household = pd.read_csv("../../join/pums_to_household_norm/household_normalized_renamed.csv")
pums = pd.read_csv("../../join/pums_to_household_norm/join_features_normalized.csv")

for column in household:
    if column in pums:
        print(column)
        household_array = np.nan_to_num(household[column].as_matrix())
        pums_array = np.nan_to_num(pums[column].as_matrix())
        print(np.histogram(household_array))
        print(np.histogram(pums_array))