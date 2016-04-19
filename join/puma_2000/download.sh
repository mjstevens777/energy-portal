#!/bin/bash
cd puma_2000

mkdir -p data
cd data
wget --recursive --no-parent \
  --continue -A 'shp.zip' http://www2.census.gov/geo/tiger/PREVGENZ/pu/


mkdir -p zip
for f in $(find www2.census.gov -name '*shp.zip')
do
	newf=zip/$(basename $f)
	cp $f $newf
done

rm -r www2.census.gov

mkdir -p shp
rm -r shp/*
for f in $(ls zip)
do
	unzip zip/$f -d shp
done

rm -r zip
