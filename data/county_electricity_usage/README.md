# Schema

The table utility_service_territory describes in which counties various
utilities operate. It has the columns:
 * `utility` Utility Name
 * `utility_number` Identifier for that utility, unique in a given year
 * `fips` County FIPS Code
 * `data_year` The year the data was generated, currently 2014

# Download

Download the data from <https://dl.dropboxusercontent.com/u/17926321/county-elecricity-usage.zip> and unzip in this directory.

# Data cleaning

## Service Territory

In the 2014 folder, the file Service_Territory_2014.xls
contains the counties in which utilities operate. Match these up with the
names in the county-names directory.

Convert Service_Territory_2014.xls to Service_Territory_2014.csv.

The line `2014│12825│NorthWestern Energy LLC - (MT)│WY│Yellowstone`
should be `2014│12825│NorthWestern Energy LLC - (MT)│MT│Yellowstone`


Then run `python county-electricity-usage/process_Service_Territory_2014.py`
to generate the normalized service territories.

## Consumption Data

Combine the consumption data from all of the utilities to get consumption
and sales for every county, split up by sector.
