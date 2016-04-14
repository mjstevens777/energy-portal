# Data

Use this directory for processing and cleaning datasets. Make a new
directory for every dataset. Add intermediate files and any large data files
to the gitignore. Add final, processed data files to the source tree if
appropriate. Try to do the processing in a way that is repeatable.

## Conventions

This directory is a python package. That means that all scripts should
be run from the data directory. Use snake case for directory names and
either snake or camel case for python files (otherwise you cannot import
from these files/directories). For reasons I don't fully understand, you
may have to run your commands like `PYTHONPATH=. python path/to/src.py`
for imports to work correctly.

At the beginning of the README.md file in each directory,
add a description of the schema (table names, description of tables,
column names, descriptions of columns).

After cleaning the data, create a file `load.sh` that will load it
into the database. Run `load.sh` from the data directory, just like
python commands.

For deeper interactions with the database, use psycopg2. Use the `db.py`
file to connect to the server.
