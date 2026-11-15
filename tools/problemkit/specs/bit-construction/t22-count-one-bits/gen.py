import random


def cases():
    rng = random.Random(20261115)
    return [
        {"id": "01", "input": "11\n"},
        {"id": "02", "input": "1\n"},
        {"id": "03", "input": "0\n"},
        {"id": "04", "input": "2\n"},
        {"id": "05", "input": "9223372036854775807\n"},
        {"id": "06", "input": "4611686018427387904\n"},
        {"id": "07", "input": "6148914691236517205\n"},
        {"id": "08", "input": "1099511627776\n"},
        {"id": "09", "input": "%d\n" % rng.getrandbits(45)},
        {"id": "10", "input": "9223372036854775806\n"},
    ]
