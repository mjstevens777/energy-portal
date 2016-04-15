import csv
import json
import re

fields = [
    "Variable Name",
    "Variable Description",
    "Response Code",
    "Label",
    "Electricity End-Use Variable",
    "Natural Gas End-Use Variable",
    "Propane End-Use Variable",
    "Fuel Oil End-Use Variable",
    "Kerosene End-Use Variable",
]

variables = []
with open("household_electricity_usage/recs2009_public_codebook.csv") as f:
    for i, row in enumerate(csv.DictReader(f, fields)):
        if i < 3:
            continue
        name = row['Variable Name']
        codeText = row['Response Code']
        labelText = row['Label']
        def normalizeAndSplit(s):
            return re.sub('\n\n*', '\n', s.strip()).split('\n')
        codes = normalizeAndSplit(codeText)
        labels = normalizeAndSplit(labelText)
        if len(codes) != len(labels):
            print(name)
            print(codes)
            print(labels)
            raise Exception('bad codebook')
        codebook = [list(t) for t in zip(codes, labels)]
        variables.append({
            'name': name,
            'description': row['Variable Description'],
            'codebook': codebook,
            'position': i - 3
        })

        # Ignore end-use variables
with open("household_electricity_usage/variables.json", "w") as f:
    json.dump({'variables': variables}, f, sort_keys=True, indent=2)
