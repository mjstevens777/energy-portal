import pickle
import json
from geo import geo_features

with open("static/assets/models/kwh_model.pkl", 'rb') as f:
    kwh_model = pickle.load(f)

with open("static/assets/models/kwh_model_features.json") as f:
    features = json.load(f)

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

    outputs = {
        "user_mean": user_usage,
        "ind_grade": "A+",
        "comm_grade": "B+",
        "ind_mean": 8000,
        "ind_stddev": 0.46,
        "comm_mean": 9082,
        "national_mean": 9082,
        "comm_stddev": 0.7,
        "national_stddev": 0.700,
    }
    outputs.update(inputs)

    return outputs
