import random


def cases():
    rng = random.Random(20261115)
    return [
        {"id": "01", "input": "8\n"},
        {"id": "02", "input": "0\n"},
        {"id": "03", "input": "1\n"},
        {"id": "04", "input": "2\n"},
        {"id": "05", "input": "3\n"},
        {"id": "06", "input": "7\n"},
        {"id": "07", "input": "576460752303423488\n"},
        {"id": "08", "input": "999999999999999998\n"},
        {"id": "09", "input": "1000000000000000000\n"},
        {"id": "10", "input": "%d\n" % rng.randrange(0, 10 ** 18)},
    ]
