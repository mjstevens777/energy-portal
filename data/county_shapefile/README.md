## Schema

The table `counties_poly` contians a map of US counties, as well as some
other extra information. It has the columns:

 * `fips` County FIPS code
 * `geom` Geographical (multi)polygon for the county
 * `county_name` Name
 * `full_fips` Full FIPS code with country information
 * `sq_mi` Area in square miles
 * `designation` The kind of county, described at <https://www.census.gov/geo/reference/lsad.html>
	- `County`
	- `city`
	- `Parish` (Louisiana)
 	- `Cty&Bor` City and Borough
 	- `Muny` Municipality
	- `Muno` Municipio (Puerto Rico)
	- `Borough`
	- `CA` Census Area?
	- `NULL` Other
