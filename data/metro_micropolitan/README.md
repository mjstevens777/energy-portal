## Schema

The table `counties_metro_micro` describes for each county whether it is
part of a metropolitan or micropolitan statistical area as used in the
census. There are two columns:
 * `county_id` The FIPS code of the county
 * `metro_micro` Text taking on the values:
   - "METRO" for metropolitan statistical area
   - "MICRO" for micropolitan statistical area
   - "NONE" for neither

## Download
Download data from
<https://www.census.gov/population/metro/files/lists/2013/List1.xls>

## Process

Every county should be assigned one of the values METRO/MICRO/NONE.

METRO for Metropolitan Statistical Area
MICRO for Micropolitan Statistical Area
NONE for neither

The county-names dataset contains a complete list of counties and can be
used for generating the list of counties that are NONE

The output should contain both county name/state, and FIPS code
