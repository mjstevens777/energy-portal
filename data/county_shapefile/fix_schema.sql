BEGIN;

alter table counties_poly rename geo_id to full_fips;
alter table counties_poly add column fips text;
update counties_poly set fips=state||county;
alter table counties_poly drop constraint counties_poly_pkey;
alter table counties_poly add constraint counties_poly_pkey PRIMARY KEY (fips);
alter table counties_poly drop column gid;
alter table counties_poly drop column state;
alter table counties_poly drop column county;
alter table counties_poly rename column name to county_name;
alter table counties_poly rename column lsad to designation;
alter table counties_poly rename column censusarea to sq_mi;

COMMIT;
