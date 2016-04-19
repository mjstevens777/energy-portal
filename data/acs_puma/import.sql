drop table if exists census_tracts_to_puma_2010;
create table census_tracts_to_puma_2010(
	state_fips text,
	county_fips text,
	tract_fips text,
	puma_code text
);

\copy census_tracts_to_puma_2010 from '2010_Census_Tract_to_2010_PUMA.txt' WITH CSV HEADER ENCODING 'LATIN1';

drop table if exists puma_poly;
create table puma_poly(
	state_fips text,
	puma_code text,
	puma_name text
);

\copy puma_poly from '2010_PUMA_Names.txt' WITH CSV HEADER ENCODING 'LATIN1';

alter table census_tracts_to_puma_2010 add column puma_id text;
alter table census_tracts_to_puma_2010 add column tract_id text;
update census_tracts_to_puma_2010 set puma_id=state_fips||puma_code;
update census_tracts_to_puma_2010 set tract_id=state_fips||county_fips||tract_fips;
alter table census_tracts_to_puma_2010 add constraint census_tracts_to_puma_2010_unique_tract primary key(tract_id);

alter table puma_poly add column puma_id text;
update puma_poly set puma_id=state_fips||puma_code;
alter table puma_poly add constraint puma_poly_pkey primary key(puma_id);

 select AddGeometryColumn('puma_poly', 'geom', 4269, 'MULTIPOLYGON', 2);


update puma_poly set geom=u.geom from (
	select puma_id, ST_Multi(ST_Union(geom)) geom
	from census_tracts_to_puma_2010
	join census_tracts_poly
	using(tract_id)
	group by puma_id
) u where u.puma_id=puma_poly.puma_id;
