import os
import csv
csv_dir = 'acs_pums/data/csv'

def extract_data_single(variables, in_files, out_file):
    out_fp = open(out_file, 'w')
    writer = csv.writer(out_fp)
    writer.writerow(['puma_id'] + variables)

    for fn in in_files:
        with open(fn) as f:
            reader = csv.DictReader(f)
            for row in reader:
                puma_id = row['ST'] + row['PUMA']
                out_row = [puma_id]
                for var in variables:
                    out_row.append(row[var])
                writer.writerow(out_row)

    out_fp.close()

def extract_data(variables, out_files):
    """
    variables: {'housing': [], 'person': []}
    out_files: {'housing': '', 'person': ''}
    """
    if 'housing' in out_files:
        file_names = []
        for fn in os.listdir(csv_dir):
            if fn[4] == 'h' and fn.endswith('.csv'):
                file_names.append(os.path.join(csv_dir, fn))
        extract_data_single(
            variables['housing'],
            file_names,
            out_files['housing']
        )
    if 'person' in out_files:
        file_names = []
        for fn in os.listdir(csv_dir):
            if fn[4] == 'p' and fn.endswith('.csv'):
                file_names.append(fn)
        extract_data_single(
            variables['person'],
            file_names,
            out_files['person']
        )


if __name__ == '__main__':
    extract_data(
        {'housing': ['WGTP', 'ELEP', 'FULP', 'GASP']},
        {'housing': 'acs_pums/data/energy_usage_individual.csv'}
    )
