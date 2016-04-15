import tarfile
import json
import csv
import sys
import codecs
from collections import defaultdict

data_dir = "acs_summary/data/"

open_mode = "r:gz"
all_path = data_dir + "All_Geographies_Not_Tracts_Block_Groups.tar.gz"
all_tf = tarfile.open(all_path, open_mode)
all_datadir = "tab4/sumfile/prod/2010thru2014/group1/"

tract_path = data_dir + "Tracts_Block_Groups_Only.tar.gz"
trac_tf = tarfile.open(tract_path, open_mode)
tract_datadir = "tab4/sumfile/prod/2010thru2014/group2/"

def get_variables():
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

variables = get_variables()

def extract_data(tf, datadir, geo_file, variables, out_file):
    recordIdsByState = defaultdict(set)
    geoIdByStateAndRecord = defaultdict(dict)
    print("Processing Geography...")
    with open(geo_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            state = row["State"].lower()
            rec = str(row["Record Number"])
            geoId = row["Full FIPS"]
            recordIdsByState[state].add(rec)
            geoIdByStateAndRecord[state][rec] = geoId

    outHeader = ["Full FIPS"]
    for seq in sorted(variables.keys()):
        for pos, id in variables[seq]:
            outHeader.append(id)
    outFp = open(out_file, "w")
    outWriter = csv.DictWriter(outFp, outHeader)
    outWriter.writeheader()

    print("Listing Files...")


    members = tf.getmembers()
    membersByStateAndSeq = defaultdict(dict)
    for member in members:
        memberSeq = member.name[-11:-7]
        memberState = member.name[-13:-11].lower()
        membersByStateAndSeq[memberState][memberSeq] = member

    print("Extracting Data...")
    for state in sorted(membersByStateAndSeq.keys()):
        print(state)
        membersBySeq = membersByStateAndSeq[state]
        stateData = []
        for seq in sorted(variables.keys()):
            print(".", end="",flush=True)
            member = membersBySeq[seq]
            memberfile = tf.extractfile(member)
            memberVars = variables[seq]
            decodedfile = codecs.iterdecode(memberfile, "latin-1")
            rowCount = 0
            for row in csv.reader(decodedfile):
                recordNum = row[5]
                if recordNum not in recordIdsByState[state]:
                    continue
                rowCount += 1
                geoId = geoIdByStateAndRecord[state][recordNum]
                outData = {"Full FIPS": geoId}
                for pos, id in memberVars:
                    outData[id] = row[pos]
                if rowCount < len(stateData):
                    stateData[rowCount].update(outData)
                else:
                    stateData.append(outData)
            memberfile.close()
        print("+", end="",flush=True)
        print()
        for d in stateData:
            outWriter.writerow(d)

    outFp.close()

print("Extracting Tracts...")
extract_data(
    trac_tf,
    tract_datadir,
    "acs_summary/data/tract_geo.csv",
    variables,
    "acs_summary/data/tract.csv"
)

print("Extracting Counties...")
extract_data(
    all_tf,
    all_datadir,
    "acs_summary/data/county_geo.csv",
    variables,
    "acs_summary/data/county.csv"
)

print("Extracting Blocks...")
extract_data(
    trac_tf,
    tract_datadir,
    "acs_summary/data/block_geo.csv",
    variables,
    "acs_summary/data/block.csv"
)
