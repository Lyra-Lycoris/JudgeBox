import random


def cases():
    rng = random.Random(20261115)
    out = [
        {"id": "01", "input": "5 3\n"},
        {"id": "02", "input": "1 1\n"},
        {"id": "03", "input": "2 1\n"},
        {"id": "04", "input": "2 2\n"},
        {"id": "05", "input": "6 6\n"},
        {"id": "06", "input": "6 1\n"},
        {"id": "07", "input": "7 4\n"},
        {"id": "08", "input": "1000 %d\n" % rng.randint(1, 1000)},
        {"id": "09", "input": "1000 1\n"},
    ]
    for k in (1, 100000, 200000):
        out.append({"id": "%02d" % (len(out) + 1), "input": "200000 %d\n" % k})
    return out
