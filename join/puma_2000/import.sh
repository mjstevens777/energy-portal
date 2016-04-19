#!/bin/bash

cd puma_2000
cd data

PSQL='bash ../../../data/psql.sh'

function upload_shp {
	f="$1"
	create_or_append="$2"
	table="$3"
	field_prefix=$(basename $f | sed 's/\.shp//')
	echo 'file' "$field_prefix"_ > mapping
	echo 'i' "$field_prefix"_i >> mapping
	echo $f
	if [[ "$create_or_append" == "-d" ]]
	then
		index="-I"
	else
		index=""
	fi
	shp2pgsql -m mapping -s 4269 -W LATIN1 $create_or_append $index $f $table | $PSQL 2>&1| uniq
	if [[ "$create_or_append" == "-d" ]]
	then
		echo "alter table $table add column state_fips text;" | $PSQL
	fi
	state=$(echo $field_prefix|sed 's/p5//;s/_.*//')
	echo "update $table set state_fips='$state' where state_fips is null;" | $PSQL
	rm mapping
}

# firstshp=$(ls shp/p1*.shp | head -n 1)
# upload_shp $firstshp -d puma_2000_1_poly -I

# for f in $(ls shp/p1*.shp|tail -n +2)
# do
# 	echo
# 	upload_shp $f -a puma_2000_1_poly
# done


firstshp=$(ls shp/p5*.shp | head -n 1)
upload_shp $firstshp -d puma_2000_5_poly -I

for f in $(ls shp/p5*.shp|tail -n +2)
do
	echo
	upload_shp $f -a puma_2000_5_poly
done
