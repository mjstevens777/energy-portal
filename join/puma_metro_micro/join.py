__author__ = 'SEOKHO'

import pandas as pd
import json

metro_micro = pd.read_csv("puma_metro_micro.csv")
household = pd.read_csv("../../models/household_work_file.csv")

with open("../../models/vectorized_puma_regions/puma_list.json") as f:
    puma_mapping = json.load(f)

metro_micro_status = [None] * household.shape[0]
for index, row in household.iterrows():
    if index % 100 == 0:
        print(index)
    numPuma = 2378
    most_likely = None
    highest_weight = 0
    for puma in range(numPuma):
        puma_weight = row["puma_prob"+str(puma)]
        if puma_weight > highest_weight:
            most_likely = puma
            highest_weight = puma_weight
    mm_table_index = metro_micro[metro_micro['puma_id'] == int(puma_mapping[str(most_likely)])].index.tolist()[0]
    metro_micro_status[index] = metro_micro['metro'][mm_table_index]

concat = pd.concat((household, pd.DataFrame(metro_micro_status, columns = ["METRO"])), axis = 1)

concat.to_csv("../../models/household_work_file.csv", index = False)