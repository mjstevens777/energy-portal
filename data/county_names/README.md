## Schema

The table `counties` maps from FIPS code to county and state name.
It has the columns:
 * `fips` County FIPS Code
 * `state` e.g. NY
 * `county_name` e.g. Chambers County


## Import

Data and description at
<https://www.census.gov/geo/reference/codes/cou.html>

Save the file as county-names.csv

Run `python countyList.py` to generate processed-county-names.csv
