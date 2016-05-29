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
        if key in inputs:
            feature_vector.append(inputs[key])
        else:
            feature_vector.append(0.)

    kwh = kwh_model.predict([feature_vector])

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
