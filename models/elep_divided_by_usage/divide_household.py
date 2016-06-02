__author__ = 'SEOKHO'

import pandas as pd

household = pd.read_csv("../household_work_file.csv")

household.append(pd.DataFrame(household['ELEP'].div(household['KWH']), columns = ['ELEP/USAGE']))

del household['ELEP']

household.to_csv("../household_work_file.csv", index = False)