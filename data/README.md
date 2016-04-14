# Data

Use this directory for processing and cleaning datasets. Make a new
directory for every dataset. Add intermediate files and any large data files
to the gitignore. Add final, processed data files to the source tree if
appropriate. Try to do the processing in a way that is repeatable.

## Conventions

This directory is a python package. That means that all scripts should
be run from the data directory. Use snake case for directory names and
either snake or camel case for python files (otherwise you cannot import
from these files/directories).

At the beginning of the README.md file in each directory,
add a description of the schema (table names, description of tables,
column names, descriptions of columns).

After cleaning the data, create a file `load.sql`, `load.sh`, or
`load.py` that will load it into the database. The following template
may be helpful:

```sql
DROP TABLE IF EXISTS my_new_data;

CREATE TABLE my_new_data(
	my_new_data_id TEXT PRIMARY KEY,
	county_fips TEXT PRIMARY KEY,
	house_size DOUBLE PRECISION
	-- And so on
);

INSERT INTO my_new_data(
	my_new_data_id,
	county_fips
) VALUES
('a', '10010'),
('b', '10011'),
('c', '10012');
```

The psql `\copy` command can be used to load data into a table from
a csv file as well.
