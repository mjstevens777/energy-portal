drop table if exists utility_service_territory;

create table utility_service_territory(
	utility text,
	utility_number text,
	fips text,
	state text,
	county_name text,
	primary key(utility, fips)
);

\copy utility_service_territory from 'Service_Territory_2014_County_Normalized.csv'	WITH CSV HEADER;

alter table utility_service_territory add column data_year integer default 2014;
