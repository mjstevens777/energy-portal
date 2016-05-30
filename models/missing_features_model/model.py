__author__ = 'SEOKHO'

import pandas as pd
import numpy as np
import sys

from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.naive_bayes import GaussianNB

class MissingEntryWrapper:
    def __init__(self, full_table_file):
        self.full_table_file = full_table_file
        self.full_table = pd.read_csv(self.full_table_file)

    #nan value is anything that will return np.isnan(value) == True
    def fill(self, predict_data):
        missing_columns = []
        for index, entry in enumerate(predict_data):
            if np.isnan(entry):
                missing_columns.append(self.full_table.columns[index])
        filled_data = self.fill_columns(predict_data, missing_columns)
        return filled_data

    #predict_data should have the same columns as the full table, but the values are irrelevant
    def fill_columns(self, predict_data, missing_columns):

        predict_data.drop(missing_columns, axis = 1, inplace = True)

        models = self.make_models(missing_columns)

        X_test = predict_data.as_matrix()
        for column in missing_columns:
            column_index = list(self.full_table.columns.values).index(column)
            print(models[column].predict(X_test))
            predict_data.insert(column_index, column, models[column].predict(X_test))
        #not sure how I want to quantify the quality of predict_data
        return predict_data

    #filename, labels of missing columns
    def make_models(self, missing_columns):

        available_table = self.full_table.copy()
        #clear out the table
        for column in missing_columns:
            del available_table[column]
        available_features = available_table.as_matrix()

        clfs = {}
        #build a model for each missing column
        for column in missing_columns:
            labels = self.full_table.as_matrix(columns = [column])
            labels = np.reshape(labels, (len(labels))) #unnest the arrays
            clf = RandomForestRegressor(n_estimators = 100)
            clf.fit(available_features, labels)
            clfs[column] = clf

        return clfs


if __name__ == "__main__":
    table_file = "pums_real_elep.csv"
    table = pd.read_csv(table_file)
    example = table[0:4].copy(deep = True)
    print("Ex", example)
    example['BLD'].apply(lambda x: np.NaN)

    print(example)
    print(MissingEntryWrapper(table_file).fill(example))
