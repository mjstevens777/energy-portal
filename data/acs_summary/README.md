## ACS Summary

Data from the American Community Survey 2014 5 Year Summary File

## Data

blockgroup.txt lists the sequence numbers for which block group
data is available.

all-urls.txt lists all available urls for downloading data, created by
scraping the server.


Run download.sh to fetch all the relevant files into the `data` folder

...Run unzip.sh to unzip all of the files into `data/seq`

### Templates

Download the file
<http://www2.census.gov/programs-surveys/acs/summary_file/2014/data/2014_5yr_Summary_FileTemplates.zip>, and unzip into the folder `templates/xls`.

Convert the excel spreadsheets in `templates/xls/seq` into csv files from `templates/csv/Seq1.csv` to `templates/csv/Seq[n].csv`, and
convert `templates/xls/2014_SFGeoFileTemplate` to
`templates/csv/geo.csv`.

### Tables

tables.csv was generated from the the five year appendices
<http://www2.census.gov/programs-surveys/acs/summary_file/2014/documentation/tech_docs/ACS_2014_SF_5YR_Appendices.xls>
that are part of the technical documentation
<https://www.census.gov/programs-surveys/acs/technical-documentation/summary-file-documentation.html>
