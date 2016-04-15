import os
import json
import csv
from collections import defaultdict

def getVariables():
    with open("acs_summary/selected-variables.csv") as f:
        variableIds = list(
            filter(lambda l: len(l) > 0,
                [line.strip() for line in f.readlines()]
            )
        )
    with open("acs_summary/variables.json") as f:
        data = json.load(f)

    sequences = defaultdict(list)

    for varId in variableIds:
        variable = data["variables"][varId]
        varData = (variable["position"], variable["id"])
        sequences[variable["sequence"]].append(varData)
    for varList in sequences.values():
        varList.sort()
    return sequences

def processGeography(geoFile):
    geoIdByStateAndRecord = defaultdict(dict)

    print("Processing Geography...")
    with open(geoFile) as f:
        reader = csv.DictReader(f)
        for row in reader:
            state = row["State"].lower()
            rec = str(row["Record Number"])
            geoId = row["Full FIPS"]
            geoIdByStateAndRecord[state][rec] = geoId

    return geoIdByStateAndRecord

def openWriters(estimateFile, marginFile, variables):
    outHeader = ["Full FIPS"]
    for seq in sorted(variables.keys()):
        for pos, id in variables[seq]:
            outHeader.append(id)

    def openWriter(file):
        fp = open(file, "w")
        writer = csv.writer(fp)
        writer.writerow(outHeader)
        return {
            'writer': writer,
            'fp': fp
        }

    writers = {'estimate': openWriter(estimateFile)}
    if marginFile is not None:
        writers['margin'] = openWriter(marginFile)

    return writers

def listFiles(dataDir):
    members = os.listdir(dataDir)
    membersDict = {
        'estimate': defaultdict(dict),
        'margin': defaultdict(dict)
    }
    for member in members:
        # e.g. e20145al0102000.txt
        memberSeq = member[-11:-7]
        memberState = member[-13:-11].lower()
        estimateOrMargin = member[-19]
        path = os.path.join(dataDir, member)
        if estimateOrMargin == 'e':
            membersDict['estimate'][memberState][memberSeq] = path
        else:
            membersDict['margin'][memberState][memberSeq] = path
    return membersDict

def extractData(dataDir, geoFile, variables,
                estimateFile, marginFile=None):
    geoIdByStateAndRecord = processGeography(geoFile)

    writers = openWriters(estimateFile, marginFile, variables)

    print("Listing Files...")
    filesDict = listFiles(dataDir)

    print("Extracting Data...")
    for state in sorted(filesDict['estimate'].keys()):
        for estimateOrMargin in writers:
            print(state + " - " + estimateOrMargin)
            writeStateData(
                variables,
                filesDict[estimateOrMargin][state],
                geoIdByStateAndRecord[state],
                writers[estimateOrMargin]['writer']
            )

    for d in writers.values():
        d['fp'].close()

def writeStateData(variables, filesBySeq, geoIdByRecord, writer):
    data = []
    firstSeq = True
    for seq in sorted(variables.keys()):
        print(".", end="", flush=True)
        fileName = filesBySeq[seq]
        file = open(fileName, encoding="latin-1")
        subsetVars = variables[seq]
        rowCount = 0
        for row in csv.reader(file):
            recordNum = row[5]
            NOT_FOUND = -1
            geoId = geoIdByRecord.get(recordNum, NOT_FOUND)
            if geoId == NOT_FOUND:
                continue
            outData = [row[pos] for pos, id in subsetVars]
            if firstSeq:
                data.append([geoId] + outData)
            else:
                data[rowCount] += outData
            rowCount += 1
        firstSeq = False
        file.close()
    print()
    print("writing")
    for i, row in enumerate(data):
        if i % (int(len(data) / 20) + 1) == 0:
            print(".", end="", flush=True)
        writer.writerow(row)
    print()

def extractTracts(dataDir, variables):
    print("Extracting Tracts...")
    extractData(
        dataDir,
        "acs_summary/data/tract_geo.csv",
        variables,
        "acs_summary/data/tract.csv",
        "acs_summary/data/tract_margin.csv"
    )

def extractCounties(dataDir, variables):
    print("Extracting Counties...")
    extractData(
        dataDir,
        "acs_summary/data/county_geo.csv",
        variables,
        "acs_summary/data/county.csv",
        "acs_summary/data/county_margin.csv"
    )

def extractBlocks(dataDir, variables):
    print("Extracting Blocks...")
    extractData(
        dataDir,
        "acs_summary/data/block_geo.csv",
        variables,
        "acs_summary/data/block.csv",
        "acs_summary/data/block_margin.csv"
    )

def main():
    variables = getVariables()

    dataDir = "acs_summary/data/all/"

    allDatadir = os.path.join(dataDir, "group1")
    tractDatadir = os.path.join(dataDir, "group2")

    extractCounties(allDatadir, variables)
    extractTracts(tractDatadir, variables)
    extractBlocks(tractDatadir, variables)

if __name__ == '__main__':
    main()
