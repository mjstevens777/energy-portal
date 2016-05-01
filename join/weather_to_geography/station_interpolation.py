__author__ = 'SEOKHO'

import csv
import math
import json
from collections import defaultdict

weatherStations = []
with open("station_metadata.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        weatherStations.append(row)

tracts = []

with open("2015_Gaz_tracts_national.csv", 'r') as f:
    reader = csv.DictReader(f, delimiter = "\t")
    for row in reader:
        d = {}
        for key in row:
            d[key.strip()] = row[key]
        tracts.append(d)

#use euclidean approximation of distance
def distance(loc1, loc2): #each loc is tuple of (latitude, longitude)
    return math.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)

distanceThreshold = 1 #kind of meaningless :(
weights = defaultdict(dict)

for tract in tracts:
    tractLat = float(tract['INTPTLAT'])
    tractLong = float(tract['INTPTLONG'])
    stationDistances = []
    for station in weatherStations:
        stationLat = float(station['Latitude'])
        stationLong = float(station['Longitude'])
        dist = distance((tractLat, tractLong), (stationLat, stationLong))
        stationDistances.append((station['USAF#'], 1/dist))
    stationDistances = sorted(stationDistances, key = lambda x : x[1])
    weights[tract['GEOID']] = {}
    for i in range(5):
        weights[tract['GEOID']][stationDistances[i][0]] = stationDistances[i][1]

with open("weighted_stations_per_census_tract.json", "wb") as f:
    f.write(bytes(json.dumps(weights), "UTF-8"))
