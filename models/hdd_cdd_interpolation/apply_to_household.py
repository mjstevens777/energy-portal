__author__ = 'SEOKHO'

import pandas as pd
import numpy as np
import json

household = pd.read_csv("../pums_geography_model/household_wpuma_prob.csv", delimiter = ',')
cdd_hdd_table = pd.read_csv("cdd_hdd.csv")

cdd_list = [0] * household.shape[0]
hdd_list = [0] * household.shape[0]
for index, row in household.iterrows():
    if index % 100 == 0:
        print(index)
    numPuma = 2378
    for puma in range(numPuma):
        puma_weight = row["puma_prob"+str(puma)]
        if puma_weight > 1E-5:
            cdd = cdd_hdd_table['CDD'][puma]
            hdd = cdd_hdd_table['HDD'][puma]
            cdd_list[index] += cdd * puma_weight
            hdd_list[index] += hdd * puma_weight

concat = pd.concat((household, pd.DataFrame(cdd_list, columns = ["CDD"]), pd.DataFrame(hdd_list, columns = ['HDD'])), axis = 1)

concat.to_csv("household_cdd_hdd.csv", index = False)