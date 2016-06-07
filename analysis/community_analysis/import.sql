drop table if exists electricity_by_puma_temp;
create table electricity_by_puma_temp(
	puma_number integer,
	elec_mean real,
	elec_std real
);

\copy electricity_by_puma_temp from 'community_distributions.csv' with csv header;

drop table if exists kwh_by_puma;
create table kwh_by_puma(
	puma_id text primary key,
	elec_mean real,
	elec_std real
);

insert into kwh_by_puma
select puma_id, elec_mean, elec_std
from electricity_by_puma_temp
natural join puma_numbers;

drop table electricity_by_puma_temp;

drop table if exists kwh_by_puma_geo;
create table kwh_by_puma_geo(
	puma_id text primary key,
	elec_mean real,
	elec_std real
);

select AddGeometryColumn('kwh_by_puma_geo', 'geom', 4269, 'MULTIPOLYGON', 2);

insert into kwh_by_puma_geo
select puma_id, elec_mean, elec_std, geom
from kwh_by_puma natural join puma_poly;
