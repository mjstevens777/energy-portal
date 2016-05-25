__author__ = 'SEOKHO'

import pandas as pd
import numpy as np
import sys

from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.naive_bayes import GaussianNB

#predict_data should have the same columns as the full table, but the values are irrelevant
def run(full_table_file, predict_data, missing_columns):

    predict_data.drop(missing_columns, axis = 1, inplace = True)

    full_table = pd.read_csv(full_table_file)
    models = make_models(full_table, missing_columns)

    X_test = predict_data.as_matrix()
    for column in missing_columns:
        column_index = list(full_table.columns.values).index(column)
        print(models[column].predict(X_test))
        predict_data.insert(column_index, column, models[column].predict(X_test))
    print("Predict", predict_data)
    #not sure how I want to quantify the quality of predict_data

#filename, labels of missing columns
def make_models(full_table, missing_columns):

    available_table = full_table.copy()
    #clear out the table
    for column in missing_columns:
        del available_table[column]
    available_features = available_table.as_matrix()

    clfs = {}
    #build a model for each missing column
    for column in missing_columns:
        labels = full_table.as_matrix(columns = [column])
        labels = np.reshape(labels, (len(labels))) #unnest the arrays
        clf = RandomForestRegressor(n_estimators = 100)
        clf.fit(available_features, labels)
        clfs[column] = clf

    return clfs


if __name__ == "__main__":
    #generate an example (will be seen by training, so not accurate for cv)
    table = pd.read_csv(sys.argv[1])
    example = table[0:4].copy(deep = True)
    print("Ex", example)

    run(sys.argv[1], example, missing_columns=["BLD"])