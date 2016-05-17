__author__ = 'SEOKHO'

import json
import pandas
import numpy

with open("../../data/acs_summary/normalized_variables.json", "r") as f:
    acsVariables = json.load(f)

with open("../../data/household_electricity_usage/normalized_variables.json", "r") as f:
    householdVariables = json.load(f)

toMerge = []
with open("Fields.tsv") as f:
    for line in f:
        toMerge.append(line.strip().split("\t"))

def findAcsField(id):
    for acsField in acsVariables:
        for field in acsField['fields']:
            if type(field) == str and id in field:
                return acsField
            elif type(field) == list:
                for subfield in field:
                    if id in subfield:
                        return acsField
    return None

def findHouseholdField(id):
    for householdField in householdVariables:
        if householdField['field'] == id:
            return householdField
    return None

#for coded histograms
def linearInterpolation(edge1, edge2):
    try:
        float(edge1)
    except:
        return float(edge2)
    try:
        float(edge2)
    except:
        return float(edge1)
    return float(edge1) + float(edge2) / 2

def merge(acsField, acsFieldIndex, householdField):
    acsSection = findAcsField(acsField)
    householdSection = findHouseholdField(householdField)
    if acsSection == None:
        print("Could not find in acs", acsField)
        return None, None
    if householdSection == None:
        print("Could not find in household", householdField)
        return None, None
    mergedSection = {}
    mergedSection['description'] = acsSection['description']
    #acsInput to output function
    acsMergeFunction = None
    #household Input to Output function
    householdMergeFunction = None
    #merge everything we can to continuous, since the final model will probably do better with continuous values than bucketed histograms, and its a lot easier for us
    if acsSection['types'][acsFieldIndex] == "Continuous":
        #identity function
        acsMergeFunction = lambda x: None if ('na' in acsSection and x in acsSection['na']) else x
    elif acsSection['types'][acsFieldIndex] == "Categorical":
        acsMergeFunction = lambda x : None if ('na' in acsSection and x in acsSection['na']) else acsSection['labels'][acsFieldIndex][x]
    if householdSection['type'] == "Continuous":
        householdMergeFunction = lambda x: None if ('na' in householdSection and x in householdSection['na']) else x
    elif householdSection['type'] == "Categorical":
        householdMergeFunction = lambda x: None if ('na' in householdSection and x in householdSection['na']) else householdSection['labels'][x]
    elif householdSection['type'] == "Coded":
        householdMergeFunction = lambda x: \
            None if ('na' in householdSection and x in householdSection['na']) \
                else linearInterpolation(householdSection['edges'][householdSection['values'].index(x)], householdSection['edges'][householdSection['values'].index(x) + 1])
    return acsMergeFunction, householdMergeFunction

#field to function
acsMergeFunctions = {}
householdMergeFunctions = {}
for mergePair in toMerge:
    #not sure what to do about the acs index...
    acsMergeFunction, householdMergeFunction = merge(mergePair[0], 0, mergePair[1])
    if acsMergeFunction == None or householdMergeFunction == None:
        print("Invalid Merge", mergePair)
        exit(1)
    acsMergeFunctions[mergePair[0]] = acsMergeFunction
    householdMergeFunctions[mergePair[1]] = householdMergeFunction

#transform household data at least
householdColumns = [mergePair[1] for mergePair in toMerge]
frame = pandas.read_csv("../../data/household_electricity_usage/recs2009_public.csv", delimiter = ',', dtype = 'str')
newFrame = pandas.DataFrame(columns = householdColumns)
for rowIndex, row in frame.iterrows():
    newRow = {}
    for column in householdColumns:
        #type problem in searching for item in list--I'd write it into the lambda function but I don't know how to...
        try:
            try:
                newRow[column] = householdMergeFunctions[column](row[column])
            except:
                newRow[column] = householdMergeFunctions[column](int(row[column]))
        except:
            print("Unknown error on row", rowIndex, "column", column)
            newRow[column] = numpy.NaN
    newFrame = pandas.concat((pandas.DataFrame([list(newRow.values())], columns = householdColumns), newFrame))

newFrame.to_csv("household_processed.csv")

