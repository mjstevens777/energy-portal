(for month in `seq -w 12`
do
	echo "http://www.ncdc.noaa.gov/orders/qclcd/QCLCD2009${month}.zip"
done)|xargs -n 1 -P 4 wget -c
