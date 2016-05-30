\copy
 (select
	puma_id,
	sum(weight1 * cast(metro_micro = 'METRO' as int)) metro,
	sum(weight1 * cast(metro_micro = 'MICRO' as int)) micro,
	sum(weight1 * cast(metro_micro = 'NONE' as int)) _none
 from counties_metro_micro natural join puma_to_counties
 group by puma_id)
 to 'puma_metro_micro.csv' WITH CSV HEADER;
