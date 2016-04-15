## Census Tracts

The table `census_tracts_poly` contains a map of census tracts with some
additional identifiers.

 * `full_fips` Census GeoId
 * `geom` Census Tract boundaries as a multipolygon
 * `state_fips` 3-digit state FIPS code
 * `county_fips` 2-digit county FIPS code
 * `tract_fips` 6-digit tract code
 * `fips` 5-digit County FIPS code
 * `sq_mi` Square Miles

## Downloading

First run `download.sh`, then `unzip.sh` to download and many shapefiles
for census tract boundaries in each state.

## Processing

Run `load.sh` to load the data into the database
