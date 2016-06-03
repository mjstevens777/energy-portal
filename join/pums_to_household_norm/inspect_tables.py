__author__ = 'SEOKHO'

import pandas as pd
import numpy as np

#household = pd.read_csv("household_normalized_renamed.csv")
pums = pd.read_csv("join_features_normalized.csv")
matrix = pums.as_matrix(columns = ['FES'])
matrix = np.nan_to_num(matrix)
print(np.histogram(matrix))