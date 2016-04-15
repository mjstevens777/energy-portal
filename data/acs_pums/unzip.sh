#!/bin/bash
cd acs_pums

mkdir -p data/csv
rm data/csv/*
for housingOrPop in $(echo h p)
do
	for state in $(cat states.txt)
	do
		f="csv_${housingOrPop}${state}.zip"
		unzip data/zip/$f '*.csv' -d data/csv
	done
done
