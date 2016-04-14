#!/bin/bash
cd county_electricity_usage

bash ../psql.sh < import.sql
