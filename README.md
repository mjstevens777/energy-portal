# energy-portal
CS194 Final Project

## Database

We have postgres instance set up at `stantron2.stanford.edu`.

### Connecting

To log, install psql and run

```sh
psql -d energy_portal -U energy_portal -h stantron2.stanford.edu
```

Add the following line to the file `$HOME/.pgpass`, where `*****` is the
password.

```
stantron2.stanford.edu:5432:energy_portal:energy_portal:*********
```

### Conventions

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

Also, add a description of the schema (table names, description of tables,
column names, descriptions of columns) to the readme file in the data
directory.

Use snake case (lower case with underscores) for everything in the database.

Make field names that are unique to a dataset globally unique, and
use the same name everywhere for foreign keys so that we can easily do
natural joins without any headaches.
