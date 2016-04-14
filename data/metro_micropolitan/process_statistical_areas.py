
import csv
from collections import defaultdict

counties = defaultdict(list)
countyFIPS = {}

with open("county_names/processed-county-names.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        counties[row['State']].append(row['County'])
        countyFIPS[row['FIPS']] = (row['County'], row['State'])

countyStatus = {}
with open("metro_micropolitan/List1.csv", "r", encoding='latin-1') as f:
    reader = csv.DictReader(f)
    for row in reader:
        countyStatus[row["FIPS State Code"]+row["FIPS County Code"]] = {"MetroMicro" : "METRO" if 'metro' in row["Metropolitan/Micropolitan Statistical Area"] else "MICRO"}

for id in countyFIPS.keys():
    if len(id) > 0:
        if id not in countyStatus:
            countyStatus[id] = {}
            countyStatus[id]['MetroMicro'] = "NONE"
        countyStatus[id]['State'] = countyFIPS[id][0]
        countyStatus[id]['County'] = countyFIPS[id][1]
        countyStatus[id]['FIPS'] = id


with open("metro_micropolitan/processed.csv", "w", newline = "") as f:
    writer = csv.DictWriter(f, fieldnames = ['FIPS', 'State', 'County', "MetroMicro"])
    writer.writeheader()
    for dic in countyStatus.values():
        if "FIPS" in dic:
            writer.writerow(dic)
