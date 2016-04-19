drop table if exists puma_to_counties;
create table puma_to_counties(
	puma_id text,
	county_id text,
	weight1 double precision,
	weight2 double precision,
	primary key(puma_id, county_id)
);

create index puma_to_counties_puma_id on puma_to_counties(puma_id);
create index puma_to_counties_county_id on puma_to_counties(county_id);

insert into puma_to_counties(puma_id, county_id, weight1)
select puma_id, county_id, count(*) from
census_tracts_to_puma_2010 join
	census_tracts_poly using(tract_id)
group by puma_id, county_id;


update puma_to_counties set weight2=weight1/weight2_total
from
(
	select county_id, sum(weight1) as weight2_total
	from puma_to_counties
	group by county_id
) a
where a.county_id = puma_to_counties.county_id;

update puma_to_counties set weight1=weight1/weight1_total
from
(
	select puma_id, sum(weight1) as weight1_total
	from puma_to_counties
	group by puma_id
) a
where a.puma_id = puma_to_counties.puma_id;

\copy puma_to_counties to 'puma_to_counties/join.csv' WITH CSV HEADER;
