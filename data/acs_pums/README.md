# PUMS (Public Use Microdata Sample)

This data represents public use microdata sample data from the american
community survey

Data:
 * <https://www.census.gov/programs-surveys/acs/data/pums.html>
 * <http://www2.census.gov/programs-surveys/acs/data/pums/>

Documentation: <https://www.census.gov/programs-surveys/acs/technical-documentation/pums.html>

## Processing

Run `acs_pums/download.sh` to download the csv_hus.zip and
csv_pus.zip files. `h` stands for housing and `p` stands
for population/people.

Run `acs_pums/unzip.sh` to extract these files to
`data/csv/ss2014[h/p][state].csv`
