drop table if exists counties_metro_micro;

create table counties_metro_micro(
	county_id text primary key,
	state text,
	county text,
	metro_micro text
);

\copy counties_metro_micro from 'processed.csv' WITH CSV HEADER;

alter table counties_metro_micro drop column state;
alter table counties_metro_micro drop column county;
