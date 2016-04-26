__author__ = 'SEOKHO'

import csv


def strToFloat(value):
    if len(value.strip()) == 0:
        return 0
    return float(value)


perPuma = {}

with open("energy_by_puma.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        perPuma[row['puma_id']] = row

pumaWeights = []
with open("puma_by_county.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        pumaWeights.append(row)


energyPerCounty = {}
energyCategories = ['ELEP', 'FULP', 'GASP']

def addEntry(county):
    energyPerCounty[county] = {}
    for energyCategory in energyCategories:
        energyPerCounty[county][energyCategory] = 0

for data in pumaWeights:
    county = data['county_id']
    if county not in energyPerCounty:
        addEntry(county)
    for energyCategory in energyCategories:
        energyPerCounty[county][energyCategory] += strToFloat(perPuma[data['puma_id']][energyCategory]) * strToFloat(data['weight1'])
    energyPerCounty[county]['county_id'] = county

with open("energy_price_per_county.csv", "w", newline = '') as f:
    writer = csv.DictWriter(f, ['county_id'] + energyCategories)
    writer.writeheader()
    for row in energyPerCounty.values():
        writer.writerow(row)