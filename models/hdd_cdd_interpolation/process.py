__author__ = 'SEOKHO'

import pandas as pd
import numpy as np

pums_lat_long = pd.read_csv("../../data/cdd_hdd/puma_lat_long.tsv", delimiter = '\t')
print(pums_lat_long.columns)
pums_lat_long = pums_lat_long[['GEOID', 'INTPTLAT', 'INTPTLONG']]

cdd_hdd = pd.read_csv("../../data/cdd_hdd/30yr_with_location.csv", delimiter = ',')

data_tuples = []

#naively just take the closest station (this takes a long time)
for _, puma in pums_lat_long.iterrows():
    closest_distance = np.infty
    closest_cdd_hdd = None
    for _, station in cdd_hdd.iterrows():
        distance = np.sqrt((float(station['Lat']) - float(puma['INTPTLAT'])) ** 2 - (float(station['Lng']) - float(puma['INTPTLONG'])) ** 2)
        if distance < closest_distance:
            closest_distance = distance
            closest_cdd_hdd = (station['CDD30'], station['HDD30'])
    data_tuples.append((puma['GEOID'], closest_cdd_hdd[0], closest_cdd_hdd[1]))

pumas = [tup[0] for tup in data_tuples]
cdds = [tup[1] for tup in data_tuples]
hdds = [tup[2] for tup in data_tuples]

final_table = pd.concat((pd.DataFrame(pumas, columns = ['PUMA']), pd.DataFrame(cdds, columns = ['CDD']), pd.DataFrame(hdds, columns = ['HDD'])), axis = 1)

final_table.to_csv("cdd_hdd.csv", index = False)