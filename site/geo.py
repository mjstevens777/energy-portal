import psycopg2
import json

connection = psycopg2.connect(
    database='energy_portal',
    user='energy_portal',
    host='stantron2.stanford.edu',
)
cursor = connection.cursor()

puma_intersect_query = """
    select puma_id, puma_name, cdd, hdd
    from puma_poly
    natural join puma_cdd_hdd
    where ST_Intersects(
        geom,
        ST_SetSRID(ST_MakePoint(%s, %s), 4269)
    );
"""

puma_nearest_query = """
    select puma_id, puma_name, cdd, hdd
    from puma_poly
    natural join puma_cdd_hdd
    order by geom <-> ST_SetSRID(ST_MakePoint(%s, %s), 4269)
    limit 1;
"""

county_intersect_query = """
    select county_id, metro_micro
    from counties_poly
    natural join counties_metro_micro
    where ST_Intersects(
        geom,
        ST_SetSRID(ST_MakePoint(%s, %s), 4269)
    );
"""

county_nearest_query = """
    select county_id, metro_micro
    from counties_poly
    natural join counties_metro_micro
    order by geom <-> ST_SetSRID(ST_MakePoint(%s, %s), 4269)
    limit 1;
"""

with open('../models/vectorized_puma_regions/puma_list.json') as f:
    puma_numbers_reverse = json.load(f)
    puma_numbers = dict(
        (int(value), key) for key, value
        in puma_numbers_reverse.items()
    )

def geo_features(lat, lng):
    features = {}

    cursor.execute(puma_intersect_query % (lng, lat))
    puma_row = cursor.fetchone()
    if puma_row is None:
        cursor.execute(puma_nearest_query % (lng, lat))
        puma_row = cursor.fetchone()
    connection.commit()

    if puma_row is None:
        raise Exception("No PUMA found")

    features['puma_id'] = puma_row[0]
    features['puma_name'] = puma_row[1]
    puma_number = puma_numbers[int(puma_row[0])]
    features['puma_prob' + puma_number] = 1.0
    features['CDD'] = puma_row[2]
    features['HDD'] = puma_row[3]

    cursor.execute(county_intersect_query % (lng, lat))
    county_row = cursor.fetchone()
    if county_row is None:
        cursor.execute(county_nearest_query % (lng, lat))
        county_row = cursor.fetchone()
    connection.commit()

    features['county_id'] = county_row[0]
    features['metro_micro'] = county_row[1]

    print(features)
    return features
