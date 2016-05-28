
def model(inputs):
    outputs = {
        "ind_grade": "A+",
        "comm_grade": "B+",
        "ind_mean": 11000,
        "comm_mean": 11050,
        "national_mean": 11100,
        "ind_stddev": 1,
        "comm_stddev": 2,
        "national_stddev": 4,
    }
    outputs.update(inputs)

    return outputs
