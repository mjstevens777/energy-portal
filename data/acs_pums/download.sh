#!/bin/bash
cd acs_pums

mkdir -p data/zip
(for housingOrPop in $(echo h p)
do
	for state in $(cat states.txt)
	do
		echo "csv_${housingOrPop}${state}.zip"
	done
done) | xargs -I{} -n 1 -P 5 wget -c "http://www2.census.gov/programs-surveys/acs/data/pums/2014/5-Year/"{} -O data/zip/{}
