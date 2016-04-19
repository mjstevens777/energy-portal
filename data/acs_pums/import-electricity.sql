drop table if exists energy_by_puma;
create table energy_by_puma(
	puma_id text,
	electricity_cost double precision,
	gas_cost double precision,
	fuel_cost double precision
);

\copy energy_by_puma from 'acs_pums/data/energy_by_puma.csv' with csv header;

insert into energy_by_puma
		select puma_id from puma_poly
		where puma_id not in (select puma_id from energy_by_puma);

select AddGeometryColumn('energy_by_puma', 'geom', 4269, 'MULTIPOLYGON', 2);

update energy_by_puma set geom=p.geom
	from puma_poly p
	where p.puma_id=energy_by_puma.puma_id;
