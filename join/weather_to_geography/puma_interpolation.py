__author__ = 'SEOKHO'

import csv
import numpy as np
import psycopg2

weatherStations = []
with open("station_metadata.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        weatherStations.append(row)

connection = psycopg2.connect("dbname='energy_portal' user='energy_portal' host='stantron2.stanford.edu'")
cursor = connection.cursor()

station_ids = []
station_lats = []
station_lngs = []
for station in weatherStations:
    station_ids.append(station['USAF#'])
    station_lats.append(float(station['Latitude']))
    station_lngs.append(float(station['Longitude']))

station_lngs = np.array(station_lngs)
station_lats = np.array(station_lats)

puma_ids = []
puma_lats = []
puma_lngs = []
cursor.execute("select puma_id, ST_X(ST_Centroid(geom)), ST_Y(ST_Centroid(geom)) from puma_poly")
for puma_id, lng, lat in cursor.fetchall():
    puma_ids.append(puma_id)
    if lat is None:
        continue
    puma_lats.append(lat)
    puma_lngs.append(lng)

puma_ids = np.array(puma_ids)
puma_lats = np.array(puma_lats)
puma_lngs = np.array(puma_lngs)

join_weights = []
join_weights_dict = {}
lines = []

for lat, lng, puma_id in zip(puma_lats, puma_lngs, puma_ids):
    dlat = station_lats - lat
    dlng = station_lngs - lng
    lng_scale = np.cos(lat * np.pi / 180.)
    dist = np.sqrt(dlat**2 + (dlng*lng_scale)**2)
    order = np.argsort(dist)[:5]
    weight = 1. / (dist + 1e-8)
    ordered_weight = weight[order]
    order = order[ordered_weight / np.sum(ordered_weight) > .1]
    total_weight = np.sum(weight[order])
    weights_dict = {}
    for i in order:
        join_weights.append((
            puma_id, station_ids[i], weight[i] / total_weight
        ))
        weights_dict[station_ids[i]] = weight[i]
        lines += [[lng, station_lngs[i]], [lat, station_lats[i]]]
    join_weights_dict[puma_id] = weights_dict

with open('puma_station_weights.csv', 'w') as f:
    weight_writer = csv.writer(f)
    weight_writer.writerow(['puma_id', 'station_id', 'weight'])
    weight_writer.writerows(join_weights)

# import json
# with open('puma_station_weights.json', 'w') as f:
#     json.dump(join_weights_dict, f, sort_keys=True, indent=2)
