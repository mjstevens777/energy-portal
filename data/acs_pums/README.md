# PUMS (Public Use Microdata Sample)

This data represents public use microdata sample data from the american
community survey

Data:
 * <https://www.census.gov/programs-surveys/acs/data/pums.html>
 * <http://www2.census.gov/programs-surveys/acs/data/pums/>

Documentation: <https://www.census.gov/programs-surveys/acs/technical-documentation/pums.html>

## Processing

Run `acs_pums/download.sh` to download the csv_h**.zip and
csv_p**.zip files. `h` stands for housing and `p` stands
for population/people and the ** will be the state.

Run `acs_pums/unzip.sh` to extract these files to
`data/csv/ss2014[h/p][state].csv`

## Metadata

Download the data dictionary from:
<http://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2010-2014.txt>

Run `python acs_pums/parse_data_dictionary.py` to generate the file
data-dictionary.json.
