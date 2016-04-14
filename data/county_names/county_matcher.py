__author__ = 'SEOKHO'

"""Defines the function match(), which will try its best to match a given county name and state code to the reference list
the current implementation might be a bit overkill, but better to have it more robust than necessary than find
inadequacies later
"""

import csv
from collections import defaultdict, Counter
import math
from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

discardPhrases = [
        "county",
        "borough",
        "parish",
        "census area",
        "municipality",
        "city and borough",
        "municipio",
		"district"
]

def normalize(county):
    county = county.lower()
    for discardPhrase in discardPhrases:
        county = county.replace(discardPhrase, "").strip()
    return county

def loadData():
    counties = defaultdict(list)
    with open("county_names/processed-county-names.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            counties[row['State']].append(row['County'])
    return counties


def calculateTf(counties):
    tf = {}
    bagOfWords = Counter()
    for state, countyList in counties.items():
        for county in countyList:
            bagOfWords.update(normalize(county).split())

    totalWords = sum(bagOfWords.values())
    for word in bagOfWords:
        #use log term frequencies to emphasize matching names over common terms
        tf[word] = math.log(float(bagOfWords[word]) / totalWords)
    return tf

counties = loadData()
tf = calculateTf(counties)

def distance(county, ref):
    county = normalize(county)
    ref = normalize(ref)
    countyWords = set(county.split())
    refWords = set(ref.split())
    intersectionWords = countyWords.intersection(refWords)
    if len(intersectionWords) > 0:
        tfScore = sum(tf[word] for word in intersectionWords) + 3.0
    else:
        tfScore = 0
    editDistance = 1 - SequenceMatcher(None, county, ref).quick_ratio()
    editDistance *= (len(county) + len(ref)) / 2.0
    editDistance = min(editDistance, 5)  # Clip to [0, 5]
    editScore = 0.3 * (editDistance - 1.5)  # (Pass if 1 character different)
    return tfScore + editScore

def match(countyName, stateCode=None):
    """Returns the reference name of the county, returns None if no match is found."""

    referenceList = counties[stateCode]
    scored = []
    for possibleMatch in referenceList:
        scored.append((possibleMatch, distance(countyName, possibleMatch)))
    scored.sort(key = lambda x : x[1])
    if scored[0][1] < 0:
        return scored[0][0]
    else:
        print("Could not find %s, %s" % (countyName, stateCode))
        return None

#tests
if __name__ == "__main__":
    print(match("Yavapai County", "AZ"))
    print(match("Yavapai", "AZ"))
    print(match("Yavapai ", "AZ"))
    print(match("Yavapai ", "CA"))
    #didn't add spell checking
    print(match("Yavpai ", "AZ"))
    print(match("Accomack", "VA"))
    #something a little harder
    print(match("Prince of Wales Ketchikan", "AK"))
