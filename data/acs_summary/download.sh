#!/bin/bash
cd acs_summary

mkdir -p data
cd data
wget -c http://www2.census.gov/programs-surveys/acs/summary_file/2014/data/5_year_entire_sf/2014_ACS_Geography_Files.zip
wget -c http://www2.census.gov/programs-surveys/acs/summary_file/2014/data/5_year_entire_sf/All_Geographies_Not_Tracts_Block_Groups.tar.gz
wget -c http://www2.census.gov/programs-surveys/acs/summary_file/2014/data/5_year_entire_sf/Tracts_Block_Groups_Only.tar.gz



# block_or_other='Tracts_Block_Groups_Only'

# # Select only sequences with block group data
# # patt=$(cat blockgroup.txt|sed 's/\(.*\)/\1000.zip/'|tr '\n' ','|sed 's/,*$//;s/\(.*\)/(\1)$/;s/,/|/g')

# # Select all sequences
# patt='000.zip$'
# tracturls=$(cat all-urls.txt|grep -E "$patt"|grep 'Tracts_Block_Groups_Only')
# otherurls=$(cat all-urls.txt|grep -E "$patt"|grep 'All_Geographies_Not_Tracts_Block_Groups')
# geourls=$(cat all-urls.txt|grep "g20145"|grep "csv"|grep 'Tracts_Block_Groups_Only')

# mkdir -p data/tract
# cd data/tract
# echo $tracturls|xargs -P 8 -n 1 wget -c

# cd ../../
# mkdir -p data/other
# cd data/other
# echo $otherurls|xargs -P 8 -n 1 wget -c

# cd ../../
# mkdir -p data/geography
# cd data/geography
# echo $geourls|xargs -P 8 -n 1 wget -c

