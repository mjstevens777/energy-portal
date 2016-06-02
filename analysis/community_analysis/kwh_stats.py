__author__ = 'SEOKHO'

import pandas as pd
import numpy as np
from scipy.stats import norm

class KWHStats:
    def __init__(self, table_file, kwh_column):
        self.table = pd.read_csv(table_file)
        self.kwh_column = kwh_column

    def national_histogram(self, bins = 10):
        return self.custom_histogram(select_params = {}, bins = bins)

    def puma_histogram(self, puma, bins = 10):
        return self.custom_histogram(select_params = {'PUMA' : puma}, bins = bins)

    def national_percentile(self, kwh):
        return self.custom_percentile(select_params = {}, kwh = kwh)

    def puma_percentile(self, puma, kwh):
        return self.custom_percentile(select_params = {'PUMA' : puma}, kwh = kwh)

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

    def select_by(self, select_params):
        selection = self.table
        for column, value in select_params.items():
            selection = selection.loc[self.table[column] == value]
        return selection[self.kwh_column]

    def custom_histogram(self, select_params, bins = 10):
        selection = self.select_by(select_params)
        return np.histogram(self.df_to_matrix(selection), bins = bins)

    def custom_percentile(self, select_params, kwh):
        selection = self.select_by(select_params)
        return np.percentile(selection, kwh)

    def fit_normal_dist(self, select_params):
        return norm.fit(self.df_to_matrix(self.select_by(select_params)))

if __name__ == "__main__":
    #histograms are skewed to filter for only < 12000kwh/year to filter out any non-households
    #unzip the .7z here
    kwh_stats = KWHStats("../../models/append_kwh/pums_kwh.csv", kwh_column = "KWH_MODELED")
    #kwh_stats = KWHStats("../../models/household_work_file.csv", kwh_column = "KWH")
    #print(kwh_stats.custom_histogram({}))
    print(kwh_stats.custom_histogram({'ST' : 13}, bins = 30))
    print(kwh_stats.fit_normal_dist({'ST' : 13}))
    print(kwh_stats.custom_histogram({'MV' : 3}, bins = 15))
