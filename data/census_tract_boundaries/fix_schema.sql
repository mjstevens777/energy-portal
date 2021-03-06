alter table census_tracts_poly rename column state to state_fips;
alter table census_tracts_poly rename column county to county_fips;
alter table census_tracts_poly rename column tract to tract_fips;

alter table census_tracts_poly add column tract_id text;
update census_tracts_poly set tract_id=state_fips||county_fips||tract_fips;
alter table census_tracts_poly drop constraint census_tracts_poly_pkey;
alter table census_tracts_poly add constraint census_tracts_poly_pkey PRIMARY KEY (tract_id);
alter table census_tracts_poly drop column gid;
alter table census_tracts_poly add column county_id text;
update census_tracts_poly set county_id=state_fips||county_fips;
alter table census_tracts_poly drop column lsad;
alter table census_tracts_poly drop column name;
alter table census_tracts_poly rename column censusarea to sq_mi;
