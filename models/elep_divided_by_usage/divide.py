__author__ = 'SEOKHO'

import pickle
import pandas as pd
import numpy as np

#divides elep (electricity bill used) by the amount of electricity used
pums = pd.read_csv("../predict_pums/pums_kwh.csv", delimiter = ',')

print(pums['ELEP'])
print(pums['KWH_MODELED'])
pums.append(pd.DataFrame(pums['ELEP'].div(pums['KWH_MODELED']), columns = ['ELEP/USAGE']))

pums.to_csv("pums_real_elep.csv")

