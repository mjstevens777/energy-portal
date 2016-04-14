#!/bin/bash
cd county_shapefile

shp2pgsql -s 4269 -W LATIN1 -d -I gz_2010_us_050_00_20m.shp counties_poly | bash ../psql.sh
bash ../psql.sh < fix_schema.sql
