__author__ = 'SEOKHO'

import countyMatcher
import csv

utilities = []
with open("county-electricity-usage/Service_Territory_2014.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        utilities.append({'Utility' : row['Utility Name'], 'State' : row['State'], 'County' : row['County']})

for utility in utilities:
    utility['County'] = countyMatcher.match(utility['County'], utility['State'])

with open("county-electricity-usage/Service_Territory_2014_County_Normalized.csv", "w", newline = '') as f:
    writer = csv.DictWriter(f, fieldnames = ['Utility', 'State', 'County'])
    writer.writeheader()
    for index, dic in enumerate(utilities):
        writer.writerow(dic)