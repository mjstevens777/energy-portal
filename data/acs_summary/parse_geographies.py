import os
import csv

with open("acs_summary/templates/csv/geo.csv") as f:
    geo_headers = f.readline().strip().split(",")

geo_dir = "acs_summary/data/geography"

out_headers = ["State", "Record Number", "Full FIPS", "Summary Level", "Name"]

# State = 040
# County = 050
# Tract = 140
# Block Group = 150
out_files = {
    "050": open("acs_summary/data/county_geo.csv", "w"),
    "140": open("acs_summary/data/tract_geo.csv", "w"),
    "150": open("acs_summary/data/block_geo.csv", "w")
}

writers = {}
for summary_level, file in out_files.items():
    writers[summary_level] = csv.DictWriter(file, out_headers)
    writers[summary_level].writeheader()

for fn in sorted(os.listdir(geo_dir)):
    if not fn.endswith(".csv"):
        continue
    path = os.path.join(geo_dir, fn)
    with open(path, encoding="latin-1") as f:
        reader = csv.DictReader(f, geo_headers)
        for row in reader:
            state = row['STUSAB']
            geo_id = row['GEOID']
            name = row['NAME']
            record_number = row['LOGRECNO']
            summary_level = row['SUMLEVEL']

            d = dict(zip(out_headers, (state, record_number, geo_id, summary_level, name)))
            if summary_level in writers:
                writers[summary_level].writerow(d)
