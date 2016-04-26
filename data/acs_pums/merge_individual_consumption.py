__author__ = 'SEOKHO'

import csv
from collections import defaultdict

def strToInt(value):
    if len(value.strip()) == 0:
        return 0
    return int(value)

perPuma = defaultdict(list)

with open("energy_usage_individual.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        perPuma[row['puma_id']].append(row)

energyCategories = ['ELEP', 'FULP', 'GASP']

composite = []
for puma_id, energyDict in perPuma.items():
    datumDict = {}
    datumDict['puma_id'] = puma_id
    for energyCategory in energyCategories:
        datumDict[energyCategory] = 0
    totalWeight = 0
    for entry in energyDict:
        weight = float(entry['WGTP'])
        totalWeight += weight
        for energyCategory in energyCategories:
            if strToInt(entry[energyCategory]) > 3:
                datumDict[energyCategory] += weight * int(entry[energyCategory])
    for energyCategory in energyCategories:
        datumDict[energyCategory] = datumDict[energyCategory] / totalWeight
    composite.append(datumDict)



with open("energy_usage_per_puma.csv", "w", newline = '') as f:
    writer = csv.DictWriter(f, ['puma_id'] + energyCategories)
    writer.writeheader()
    for point in composite:
        writer.writerow(point)
