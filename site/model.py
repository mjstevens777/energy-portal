import pickle
import json

with open("static/assets/models/kwh_model.pkl") as f:
    kwh_model = pickle.load(f)

with open("static/assets/models/kwh_model_features.json") as f:
    features = json.load(f)

def model(inputs):
    feature_vector = []
    for feature in features:
        key = feature.lower()
        if key in inputs and inputs[key] is not None and inputs[key] != '':
            print("Found %s" % key)
            print(inputs[key])
            feature_vector.append(float(inputs[key]))
        else:
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
