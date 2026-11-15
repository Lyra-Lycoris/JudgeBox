import random

rng = random.Random(20261120)


def cases():
    out = [
        {"id": "01", "input": "6 2\n"},
        {"id": "02", "input": "2 1\n"},
        {"id": "03", "input": "4 1\n"},
        {"id": "04", "input": "4 2\n"},
        {"id": "05", "input": "10 5\n"},
        {"id": "06", "input": "8 3\n"},
        {"id": "07", "input": "100 1\n"},
        {"id": "08", "input": "1000 500\n"},
        {"id": "09", "input": "1000 %d\n" % rng.randint(1, 500)},
        {"id": "10", "input": "200000 1\n"},
        {"id": "11", "input": "200000 100000\n"},
        {"id": "12", "input": "200000 3\n"},
    ]
    return out
