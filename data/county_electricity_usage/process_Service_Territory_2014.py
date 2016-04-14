__author__ = 'SEOKHO'

from county_names.county_matcher import match as matchCounty
import csv

utilities = []
with open("county_electricity_usage/Service_Territory_2014.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        utilities.append({
            'Utility' : row['Utility Name'],
            'UtilityID': row['Utility Number'],
            'State' : row['State'],
            'County' : row['County']
        })

for utility in utilities:
    utility['County'], utility['FIPS'] = matchCounty(utility['County'], utility['State'])

with open("county_electricity_usage/Service_Territory_2014_County_Normalized.csv", "w", newline = '') as f:
    writer = csv.DictWriter(f, fieldnames=['Utility', 'UtilityID', 'FIPS', 'State', 'County'])
    writer.writeheader()
    for index, dic in enumerate(utilities):
        writer.writerow(dic)
