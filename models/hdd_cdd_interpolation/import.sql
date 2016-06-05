drop table if exists puma_cdd_hdd_temp;
drop table if exists puma_cdd_hdd;

create table puma_cdd_hdd_temp(
	puma_id_float real,
	cdd real,
	hdd real
);

\copy puma_cdd_hdd_temp from 'cdd_hdd.csv' WITH CSV HEADER

create table puma_cdd_hdd(
	puma_id text primary key,
	cdd real,
	hdd real
);

insert into puma_cdd_hdd
	select puma_id, cdd, hdd
	from puma_cdd_hdd_temp, puma_poly
	where puma_id_float::integer = puma_id::integer;
