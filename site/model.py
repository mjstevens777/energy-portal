import pickle
import json
from geo import geo_features
import os
import scipy.stats as st
import numpy as np

model_dir = "../models/kwh_model"

with open(os.path.join(model_dir, "kwh_model.pkl"), 'rb') as f:
    kwh_model = pickle.load(f)

with open(os.path.join(model_dir, "kwh_model_features.json")) as f:
    features = json.load(f)
    for i in range(2378):
        features.append("puma_prob%d" % i)

def model(inputs):
    feature_vector = []

    inputs.update(
        geo_features(inputs['lat'], inputs['lng'])
    )

    for feature in features:
        key = feature.lower()
        if key in inputs and inputs[key] is not None and inputs[key] != '':
            print("Found %s" % key)
            print(inputs[key])
            feature_vector.append(float(inputs[key]))
        else:
            if not key.startswith('puma'):
                print("Missing: %s" % key)
            feature_vector.append(0.)

    kwh = kwh_model.predict([feature_vector])[0]
    print(kwh)

    user_usage = float(inputs['elep']) / float(inputs['eler']) * 12.0

    ind_grade = "A+"
    comm_grade = "B+"

    outputs = {
        "user_mean": user_usage,

        "ind_grade": ind_grade,
        "comm_grade": comm_grade,

        "ind_mean": kwh,
        "ind_stddev": 0.46,

        "national_mean": 9082,
        "national_stddev": 0.700,
    }

    z_score = (np.log(outputs['user_mean']) - np.log(outputs['national_mean']))
    z_score /= outputs['national_stddev']
    percentile = 1 - st.norm.cdf(z_score)
    def grade(percentile):
        if percentile > 0.8:
            return "A"
        elif percentile > 0.5:
            return "B"
        elif percentile > 0.2:
            return "C"
        else:
            return "D"
    outputs['ind_grade'] = grade(percentile)

    outputs.update(inputs)

    return outputs
