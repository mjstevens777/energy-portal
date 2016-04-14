cd census_tract_boundaries
mkdir -p zip
cd zip

(for i in `seq 1 72`
do
  statefips=$(printf "%02d" "$i")
  echo $statefips
done)|xargs -n 1 -P 8 -I{} curl -s -f -o "{}.zip" "http://www2.census.gov/geo/tiger/GENZ2010/gz_2010_{}_140_00_500k.zip"
