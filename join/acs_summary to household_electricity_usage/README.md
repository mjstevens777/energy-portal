5/17/2016 --

Uses normalized_variables.json for acs_summary and household_electricity_usage to normalize values in each dataset
to be comparable with the values from the other. 

Basic documentation: 
-Fields.tsv indicate the pairs of fields to be merged
-Function "merge" takes the ids of each (and the index for acs, which is assumed 0 here) and returns
two functions, which normalize the raw value from acs_summary and household_electricty_usage respectively

Some (possible) limitations:
1. No checking for similar, non-identical overlaps between categories
2. Histogram buckets are naively converted into continuous values
3. The combining does not have the data from each dataset interact with each other to devise a more appropriate method of combining

Current product: A normalized output for the selected variables in household_electricty_usage 

Todo: Match it against acs_summary and debug, figure out why some values are out of bounds? ("Unknown Errors")