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

    outputs = {
        "ind_grade": "A+",
        "comm_grade": "B+",
        "ind_mean": kwh,
        "comm_mean": kwh + 50,
        "national_mean": kwh + 100,
        "ind_stddev": 1,
        "comm_stddev": 2,
        "national_stddev": 4,
    }
    outputs.update(inputs)

    return outputs
