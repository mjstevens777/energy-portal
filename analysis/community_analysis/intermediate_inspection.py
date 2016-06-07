__author__ = 'SEOKHO'

import pandas as pd
import numpy as np

pums = pd.read_csv("../../join/pums_to_household_norm/join_features_normalized.csv")
household = pd.read_csv("../../join/pums_to_household_norm/household_normalized_renamed.csv")

print(np.histogram(household['PUMA'], bins = 100))
print(np.histogram(pums['PUMA'], bins = 100))