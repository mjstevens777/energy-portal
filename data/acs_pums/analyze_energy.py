import csv
from collections import defaultdict

vars = ['ELEP', 'GASP', 'FULP']

data = {}
for var in vars:
    data[var] = defaultdict(float)
    data[var + '_weight'] = defaultdict(float)

puma_ids = set()

with open('acs_pums/data/energy_usage_individual.csv') as f:
    for i, row in enumerate(csv.DictReader(f)):
        if i % 10000 == 0:
            print('.', end='', flush=True)
        puma_id = row['puma_id']
        puma_ids.add(puma_id)
        for var in ['ELEP', 'GASP', 'FULP']:
            value = row[var]
            if value.isdigit() and int(value) >= 4:
                weight = float(row['WGTP'])
                data[var][puma_id] += float(value) * weight
                data[var + '_weight'][puma_id] += weight

with open('acs_pums/energy_by_puma.csv', 'w') as f:
    writer = csv.DictWriter(f, ['puma_id'] + vars)
    writer.writeheader()
    for puma_id in puma_ids:
        row = {'puma_id': puma_id}
        for var in vars:
            if puma_id in data[var]:
                row[var] = data[var][puma_id] / data[var + '_weight'][puma_id]
            else:
                row[var] = None
        writer.writerow(row)


