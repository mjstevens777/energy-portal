cd census_tract_boundaries

mkdir -p shp
cd zip
ls|xargs -I{} -n 1 -P 4 unzip {} -d ../shp
