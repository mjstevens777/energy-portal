
def model(inputs):
    outputs = {
        "ind_grade": "A+",
        "comm_grade": "B+",
        "ind_mean": 11000,
        "comm_mean": 11050,
        "national_mean": 11100,
        "ind_var": 1,
        "comm_var": 2,
        "national_var": 4,
    }
    outputs.update(inputs)

    return outputs
