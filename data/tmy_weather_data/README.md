## Schema

This dataset represents a typical year of hourly weather at many US locations.

## Download

Data and descriptions can be found at <http://rredc.nrel.gov/solar/old_data/nsrdb/1991-2005/tmy3/>.

## Processing

This data is really big. Be careful not to put it check it into git. Modify
the .gitignore file appropriately.

Parse the metadata in the files and create a table weather_stations
describing these stations (name/id/location/etc.)

Create a table weather_summary that links stations by id to summary statistics
about the weather at these locations. To start with, generate the statistics
for heating degree days (hdd) and cooling degree days (cdd) and insert these
into the weather_summary table

Optionally, put the raw data in a table called weather_datapoints.
You can either use a primary key of `(station id, hour)` to reference the data,
or use a primary key of `station id` and store the data in arrays.
Again, this is a lot of data, so only store the useful stuff.

## Processing Methods (Seokho)

process_tmy.py contains methods to process metadata (straightforward) and to extract
columns from the tmy data. The current method hashes each set of data points to a key
(station #, date, hour). There is no load script yet because the data is so enormous
I would rather not load useless data just for the sake of testing.

TODO: Load scripts after figuring out what we need.