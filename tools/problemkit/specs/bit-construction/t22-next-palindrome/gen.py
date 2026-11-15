import random


def cases():
    rng = random.Random(20261115)
    return [
        {"id": "01", "input": "1234\n"},
        {"id": "02", "input": "0\n"},
        {"id": "03", "input": "1\n"},
        {"id": "04", "input": "9\n"},
        {"id": "05", "input": "10\n"},
        {"id": "06", "input": "11\n"},
        {"id": "07", "input": "102\n"},
        {"id": "08", "input": "999\n"},
        {"id": "09", "input": "1000\n"},
        {"id": "10", "input": "1999\n"},
        {"id": "11", "input": "1000000000000000000\n"},
        {"id": "12", "input": "%d\n" % rng.randrange(10 ** 17, 10 ** 18)},
    ]
