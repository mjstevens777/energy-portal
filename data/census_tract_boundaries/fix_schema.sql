 gid        | integer                     | not null default nextval('census_tracts_poly_gid_seq'::regclass)
 geo_id     | character varying(60)       |
 state      | character varying(2)        |
 county     | character varying(3)        |
 tract      | character varying(6)        |
 name       | character varying(90)       |
 lsad       | character varying(7)        |
 censusarea | numeric                     |

alter table census_tracts_poly rename column geo_id to full_fips;
alter table census_tracts_poly drop constraint census_tracts_poly_pkey;
alter table census_tracts_poly add constraint census_tracts_poly_pkey PRIMARY KEY (full_fips);
alter table census_tracts_poly drop column gid;
alter table census_tracts_poly add column fips text;
update census_tracts_poly set fips=state||county;
alter table census_tracts_poly rename column state to state_fips;
alter table census_tracts_poly rename column county to county_fips;
alter table census_tracts_poly rename column tract to tract_fips;
alter table census_tracts_poly drop column lsad;
alter table census_tracts_poly rename column censusarea to sq_mi;
