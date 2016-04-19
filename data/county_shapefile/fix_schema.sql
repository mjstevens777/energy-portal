BEGIN;

alter table counties_poly add column county_id text;
update counties_poly set county_id=state||county;
alter table counties_poly drop constraint counties_poly_pkey;
alter table counties_poly add constraint counties_poly_pkey PRIMARY KEY (county_id);
alter table counties_poly drop column gid;
alter table counties_poly drop column state;
alter table counties_poly drop column county;
alter table counties_poly rename column name to county_name;
alter table counties_poly rename column lsad to designation;
alter table counties_poly rename column censusarea to sq_mi;

COMMIT;
