__author__ = 'SEOKHO'

import pandas as pd
import numpy as np
from scipy.stats import norm

class KWHStats:
    def __init__(self, table_file, kwh_column, log):
        self.table = pd.read_csv(table_file)
        self.kwh_column = kwh_column
        self.log = log
        if log:
            self.table[self.kwh_column] = np.log(self.table[self.kwh_column])

    def national_histogram(self, bins = 10):
        return self.histogram(select_params = {}, bins = bins)

    def puma_histogram(self, puma, bins = 10):
        return self.histogram(select_params = {'PUMA' : puma}, bins = bins)

    def national_percentile(self, kwh):
        return self.percentile(select_params = {}, kwh = kwh)

    def puma_percentile(self, puma, kwh):
        return self.percentile(select_params = {'PUMA' : puma}, kwh = kwh)

    def df_to_matrix(self, df):
        matrix = df.as_matrix()
        matrix = np.nan_to_num(matrix)
        return self.filter_for_individual_households(matrix)

    def filter_for_individual_households(self, array):
        filtered = []
        for val in array:
            if val < 2000 * 12: #kwh/year
                filtered.append(val)
        return filtered

    def select_by(self, select_params = None):
        if select_params is None:
            select_params = {}
        selection = self.table
        for column, value in select_params.items():
            selection = selection.loc[self.table[column] == value]
        return selection[self.kwh_column]

    def histogram(self, select_params = None, bins = 10):
        selection = self.select_by(select_params)
        return np.histogram(self.df_to_matrix(selection), bins = bins)

    def percentile(self, kwh, select_params = None):
        selection = self.select_by(select_params)
        return np.percentile(selection, kwh)

    def fit_normal_dist(self, select_params = None):
        return norm.fit(self.df_to_matrix(self.select_by(select_params)))

if __name__ == "__main__":
    #histograms are skewed to filter for only < 12000kwh/year to filter out any non-households
    #unzip the .7z here
    kwh_stats = KWHStats("../../models/append_kwh/pums_kwh.csv", kwh_column = "KWH_MODELED", log = True)
    household_stats = KWHStats("../../models/household_complete_one_hot.csv", kwh_column = "KWH", log = True)
    print(kwh_stats.histogram())
    print(household_stats.histogram())
    #print(kwh_stats.custom_histogram({'ST' : 13}, bins = 30))
    #print(kwh_stats.fit_normal_dist({'ST' : 13}))
    #print(kwh_stats.custom_histogram({'MV' : 3}, bins = 15))

    import json
    with open("../../models/vectorized_puma_regions/puma_list.json") as f:
        puma_mapping = json.load(f)

    stats = []
    for puma in range(2378):
        stats.append(list(kwh_stats.fit_normal_dist({'PUMA': int(puma_mapping[str(puma)])})))
    pd.DataFrame(stats, columns = ['MEAN', 'STD']).to_csv("community_distributions.csv")
