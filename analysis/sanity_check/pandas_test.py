__author__ = 'SEOKHO'

import pandas as pd
import numpy as np

household = pd.read_csv("../../models/household_complete_one_hot.csv")
household['NEW'] = pd.DataFrame(list(np.arange(household.shape[0])), columns = ["NEW"])

print(household['NEW'].as_matrix())