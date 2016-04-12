
import csv
from collections import defaultdict

counties = defaultdict(list)
countyFIPS = {}

with open("../raw/county-names/processed-county-names.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        counties[row['State']].append(row['County'])
        countyFIPS[row['ID']] = (row['County'], row['State'])

countyStatus = {}
with open("List1.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        countyStatus[row["FIPS State Code"]+row["FIPS County Code"]] = {"STATUS" : "METRO" if 'metro' in row["Metropolitan/Micropolitan Statistical Area"] else "MICRO"}

for id in countyFIPS.keys():
    if len(id) > 0:
        if id not in countyStatus:
            countyStatus[id] = {}
            countyStatus[id]['STATUS'] = "NONE"
        countyStatus[id]['State'] = countyFIPS[id][0]
        countyStatus[id]['County'] = countyFIPS[id][1]
        countyStatus[id]['FIPS'] = id


with open("processed.csv", "w", newline = "") as f:
    writer = csv.DictWriter(f, fieldnames = ['FIPS', 'State', 'County', "STATUS"])
    writer.writeheader()
    for dic in countyStatus.values():
        if "FIPS" in dic:
            writer.writerow(dic)
