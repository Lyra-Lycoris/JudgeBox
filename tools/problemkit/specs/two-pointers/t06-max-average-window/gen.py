import random


def cases():
    rng = random.Random(20261120)
    n = 200000
    mixed = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    negatives = [-rng.randint(1, 10 ** 9) for _ in range(n)]
    pattern = [((i * 37) % 199) - 99 for i in range(n)]
    mid = [rng.randint(-1000, 1000) for _ in range(2000)]
    return [
        {"id": "01", "input": "3 2\n1 3 4\n"},
        {"id": "02", "input": "1 1\n5\n"},
        {"id": "03", "input": "4 4\n-1 -2 -3 -4\n"},
        {"id": "04", "input": "5 2\n1 12 -5 -6 50\n"},
        {"id": "05", "input": "3 3\n0 0 0\n"},
        {"id": "06", "input": "200000 1\n" + " ".join(str(x) for x in mixed) + "\n"},
        {"id": "07", "input": "200000 200000\n" + " ".join(["7"] * n) + "\n"},
        {"id": "08", "input": "2000 7\n" + " ".join(str(x) for x in mid) + "\n"},
        {"id": "09", "input": "200000 1000\n" + " ".join(str(x) for x in mixed) + "\n"},
        {"id": "10", "input": "200000 199999\n" + " ".join(str(x) for x in mixed) + "\n"},
        {"id": "11", "input": "200000 50000\n" + " ".join(str(x) for x in negatives) + "\n"},
        {"id": "12", "input": "200000 3\n" + " ".join(str(x) for x in pattern) + "\n"},
    ]
