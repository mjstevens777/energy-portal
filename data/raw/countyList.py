#Generates our reference list for all counties, and gives each one an arbitrary id

import csv

counties = []

with open("county-names/county-names.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        counties.append({'State' : row['State Postal Code'], 'County' : row['FIPS Class Code']})

with open("county-names/processed-county-names.csv", "w", newline = '') as f:
    writer = csv.DictWriter(f, fieldnames = ['State', 'County', 'ID'])
    writer.writeheader()
    for index, dic in enumerate(counties):
        dic['ID'] = index
        writer.writerow(dic)

