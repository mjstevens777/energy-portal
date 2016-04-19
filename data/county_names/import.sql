drop table if exists counties;

create table counties(
	county_id text primary key,
	state text,
	county_name text
);

\copy counties from 'processed-county-names.csv' WITH CSV HEADER
