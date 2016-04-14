"""Generates our reference list for all counties.

Gives each county an id based on its FIPS code.
"""

import csv

counties = []

with open("county_names/county-names.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        counties.append({
            'State': row['State Postal Code'],
            'County': row['FIPS Class Code'],
            'FIPS': row['State FIPS Code'] + row['County FIPS Code']
        })

with open("county_names/processed-county-names.csv", "w", newline = '') as f:
    writer = csv.DictWriter(f, fieldnames = ['FIPS', 'State', 'County'])
    writer.writeheader()
    for dic in counties:
        writer.writerow(dic)

