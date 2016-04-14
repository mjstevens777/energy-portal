cd census_tract_boundaries

firstshp=$(ls shp/*.shp|head -n 1)

echo $firstshp
shp2pgsql -s 4269 -W LATIN1 -d -I $firstshp census_tracts_poly | bash ../psql.sh | uniq

for f in $(ls shp/*.shp|tail -n +2)
do
	echo
	echo $f
	shp2pgsql -s 4269 -W LATIN1 -a $f census_tracts_poly | bash ../psql.sh | uniq
done
