__author__ = 'SEOKHO'

import pandas as pd

household = pd.read_csv("../../models/household_work_file.csv")

print(list(household['KWH']))