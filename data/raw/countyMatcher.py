__author__ = 'SEOKHO'

#important function is match(), which will try its best to match a given county name and state code to the reference list
#the current implementation might be a bit overkill, but better to have it more robust than necessary than find
#inadequacies later

import csv
from collections import defaultdict, Counter
import math

counties = defaultdict(list)

bagOfWords = Counter()

with open("county-names/processed-county-names.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        counties[row['State']].append(row['County'])
        bagOfWords.update(row['County'].split(" "))

totalWords = sum(bagOfWords.values())
tf = {}
for word in bagOfWords:
    #use log term frequencies to emphasize matching names over common terms
    tf[word] = math.log(bagOfWords[word] / totalWords)

#Returns the reference name of the county, returns None if no match is found
def match(countyName, stateCode = 'CA'):
    referenceList = counties[stateCode]
    scored = []
    for possibleMatch in referenceList:
        intersection = set(possibleMatch.split(" ")).intersection(set(countyName.split(" ")))
        score = sum([tf[word] for word in intersection])
        scored.append((possibleMatch, score))
    scored.sort(key = lambda x : x[1])
    if scored[0][1] < -5:
        return scored[0][0]
    else:
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