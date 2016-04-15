## ACS Summary

Data from the American Community Survey 2014 5 Year Summary File

## Data

blockgroup.txt lists the sequence numbers for which block group
data is available.

all-urls.txt lists all available urls for downloading data, created by
scraping the server.


Run download.sh to fetch all the relevant files into the `data` folder

### Templates

Download the file
<http://www2.census.gov/programs-surveys/acs/summary_file/2014/data/2014_5yr_Summary_FileTemplates.zip>, and unzip into the folder `templates/xls`.

Convert the excel spreadsheets in `templates/xls/seq` into csv files from `templates/csv/Seq1.csv` to `templates/csv/Seq[n].csv`, and
convert `templates/xls/2014_SFGeoFileTemplate` to
`templates/csv/geo.csv`.

### Geography

Run `acs_summary/unzip-geography.sh` to extract the geography files into
`data/geography`

Run `python acs_summary/parse_geographies.py` to extract the locations of
county, tract, and block group geographies.


### Tables

tables.csv was generated from the the five year appendices
<http://www2.census.gov/programs-surveys/acs/summary_file/2014/documentation/tech_docs/ACS_2014_SF_5YR_Appendices.xls>
that are part of the technical documentation
<https://www.census.gov/programs-surveys/acs/technical-documentation/summary-file-documentation.html>

## Variable Selection

Run `python acs_summary/generate_variable_descriptions.py` to generate the file `variables.json`. This file has the following structure:
  - `topics` Object
  	- `topics[topicId]` Object
  	  - `id` Topic Id
  	  - `groups` Array of Group Ids
  - `groups` Object
  	- `groups[groupId]` Object
  	  - `id` Group Id
  	  - `tables` Array of Table Ids
  - `tables` Object
  	- `table[tableId]` Object
  	  - `id` Table Id
  	  - `description` Table Description
  	  - `variables` Array of Variable Ids
  	  - `sequences` Sequences this table is found in
  	  - `locations` list of (sequence, startPos, endPos) tuples
  	  - `size` Number of records
  	  - `restrictions` String
  - `variables` Object
  	- `variables[variableId]` Object
  	  - `id` Variable Id
  	  - `description` Variable Description
  	  - `sequence` Sequence this variable is found in
  	  - `position` Zero-Indexed position in the sequence files

Run `python acs_summary/generate_selection_html.py` to generate the file
`select.html`.

Open `select.html` in a browser. The data is organized heirarchically. The
tables will be the entries in gray and white. They have the format:
'id - number of variables - description (restrictions)'. You can click on
the tables and they will expand to show the variables they contain. You
can select full tables or individual variables.

The outermost groups are topics - the 'B01' level. These are colored in blue.
You can collapse and expand topics by clicking on the title.

The tables are sometimes grouped together if they have the same kind of data,
such as B01001 for Sex by Age. These groups will show as green and white.
Other times, there is no grouping and the tables stand alone. These groups
can also be collapsed and expanded.

Select all of the variables that will be extracted from the files, then go
to the top and hit 'Get selections'. Paste the contents of this into
`selected-variables.csv`. If you would like to modify this selection later,
go back and hit 'Set selections' to open up a text box where you can paste
the contents of `selected-variables.csv`. Hit go to apply the selections.
This may take a while.
