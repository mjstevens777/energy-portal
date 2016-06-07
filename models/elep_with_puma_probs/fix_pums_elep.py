__author__ = 'SEOKHO'

import pandas as pd
import numpy as np

pums = pd.read_csv("../joined_weather.csv", nrows = 10000)

elep_matrix = pums['ELEP'].as_matrix()
print(elep_matrix)

for index, value in enumerate(elep_matrix):
    if value > 2:
        elep_matrix[index] = value * 12
    else:
        elep_matrix[index] = 0

del pums['ELEP']
pums['ELEP'] = pd.DataFrame(elep_matrix, columns = ['ELEP'])

print(np.histogram(pums['ELEP']))