#!/bin/bash
cd acs_summary/data

tar -xvzf All_Geographies_Not_Tracts_Block_Groups.tar.gz
tar -xvzf Tracts_Block_Groups_Only.tar.gz

mkdir -p all
mv tab4/sumfile/prod/2010thru2014/* all && rm -r tab4
