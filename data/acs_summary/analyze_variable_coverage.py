from collections import defaultdict, Counter
import csv

inputFiles = {
    "county": "acs_summary/data/county.csv",
    "tract": "acs_summary/data/tract.csv",
    "block": "acs_summary/data/block.csv",
}

outputFiles = {
    "county": "acs_summary/data/hist_county.json",
    "tract": "acs_summary/data/hist_tract.json",
    "block": "acs_summary/data/hist_block.json"
}


def isNumeric(s):
    numeric = False
    try:
        float(s)
        numeric = True
    except Exception:
        pass
    return numeric

def generateSubHistogram(values):
    histogram = Counter(values)
    outHist = defaultdict(int)
    for dataValue, count in histogram.items():
        if dataValue is None:
            dataValue = "NULL"
        thresh = len(values) / 20
        if count <= thresh and isNumeric(dataValue):
            if dataValue.isdigit():
                outHist["varied int"] += count
            else:
                outHist["varied float"] += count
        else:
            outHist[dataValue] = count
    return outHist

def generateHistogram(inputFile, outputFile):

    # histograms = defaultdict(Counter)
    transpose = defaultdict(list)
    histograms = defaultdict(Counter)

    def updateHistograms():
        for k in transpose:
            histograms[k].update(
                generateSubHistogram(transpose[k])
            )
            transpose[k].clear()

    with open(inputFile) as f:
        print("Getting Line Count...")
        total = len(f.readlines())
        numSplits = int(total / 2000) + 1
        splitSize = int(total / numSplits) + 1
        if splitSize * numSplits < total:
            raise Exception("Bad Split")

        print("Reading...")
        f.seek(0)
        for i, row in enumerate(csv.DictReader(f)):
            del row["Full FIPS"]
            for k, v in row.items():
                transpose[k].append(v)
            if (i + 1) % 1000 == 0:
                print(".", end="", flush=True)
            if (i + 1) % splitSize == 0:
                updateHistograms()
    updateHistograms()

    print("Writing...")
    import json
    with open(outputFile, "w") as f:
        json.dump(histograms, f, sort_keys=True, indent=2)

def main():
    regions = [
        "county",
        "tract",
        "block",
    ]
    for regionType in regions:
        print("Processing " + regionType + "...")
        generateHistogram(inputFiles[regionType], outputFiles[regionType])
        print()

if __name__ == '__main__':
    main()
