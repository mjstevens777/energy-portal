"""Defines connection and cursor.

To use this module, just run something like:

from db import connection, cursor
cursor.execute("update counties set fips=fips;")
connection.commit()

See https://wiki.postgresql.org/wiki/Psycopg2_Tutorial for more.
"""
import psycopg2

connection = psycopg2.connect("dbname='energy_portal' user='energy_portal' host='stantron2.stanford.edu'")
cursor = connection.cursor()

if __name__ == "__main__":
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])
