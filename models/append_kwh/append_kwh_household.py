__author__ = 'SEOKHO'

import pandas as pd

household = pd.read_csv("../household_work_file.csv")

kwh_table = pd.read_csv("../../data/household_electricity_usage/recs2009_public.csv")
kwh = kwh_table.as_matrix(columns = ['KWH'])

print(kwh.shape)

household = pd.concat((household, pd.DataFrame(kwh, columns = ['KWH'])), axis = 1)

household.to_csv("../household_work_file.csv", index = False)