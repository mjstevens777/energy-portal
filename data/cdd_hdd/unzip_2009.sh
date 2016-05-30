mkdir -p 2009

rm 2009/*

for f in $(ls *.zip)
do
	unzip $f -d 2009
	rm 2009/*hourly.txt
	rm 2009/*daily.txt
done


