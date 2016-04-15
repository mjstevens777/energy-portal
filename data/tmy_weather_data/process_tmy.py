__author__ = 'SEOKHO'

import sys
import os.path
import csv

def readMetadataLine(line):
    components = line.strip().split(",")
    return {"USAF#" : components[0], "Name" : components[1].replace("\"", ""), "State" : components[2], "TimeZone": components[3], "Latitude": components[4], "Longitude" : components[5], "Elevation": components[6]}

def parseMetadata(dir):
    stations = []
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            file = os.path.join(root, name)
            with open(file, "r") as f:
                for line in f:
                    stations.append(readMetadataLine(line))
                    break

    with open("station_metadata.csv", "w", newline = "") as f:
        writer = csv.DictWriter(f, fieldnames = ['USAF#', 'Name', 'State', 'TimeZone', 'Latitude', 'Longitude', 'Elevation'])
        writer.writeheader()
        for station in stations:
            writer.writerow(station)

#idColumns are appended to USAF# to form a datapoint, infoColumn is the weather information we are looking for
def parseDataSubset(dir, idColumns, infoColumns):
    #we'll just store it in memory, but it is big, so if needed we can change to streaming
    data = []
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            file = os.path.join(root, name)
            with open(file, "r") as f:
                metadata = readMetadataLine(f.readline())
                reader = csv.DictReader(f)
                for row in reader:
                    dic = {'key':metadata['USAF#']+','+','.join([row[col] for col in idColumns])}
                    for col in infoColumns:
                        dic[col] = row[col]
                    data.append(dic)

    with open("station_data.csv", "w", newline = "") as f:
        writer = csv.DictWriter(f, fieldnames = ['key']+infoColumns)
        writer.writeheader()
        for datum in data:
            writer.writerow(datum)


if __name__ == "__main__":
    #directory of unzipped files
    #parseMetadata(sys.argv[1])
    #to extract
    parseDataSubset(sys.argv[1], ['Date (MM/DD/YYYY)', 'Time (HH:MM)'], ['TotCld (tenths)'])