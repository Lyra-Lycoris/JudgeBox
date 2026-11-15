import random


def cases():
    rng = random.Random(20261115)
    n = 200000
    big = ["1000000000"] * n
    ones = ["1"] * n
    mid = [str(rng.randint(1, 1000)) for _ in range(n)]
    wide = [str(rng.randint(1, 10 ** 9)) for _ in range(n)]
    sparse = ["1"] * n
    for i in range(0, n, 1000):
        sparse[i] = "1000000000"
    mixed = [str(rng.randint(1, 10 ** 6)) for _ in range(n)]
    return [
        {"id": "01", "input": "6 7\n2 3 1 2 4 3\n"},
        {"id": "02", "input": "1 6\n5\n"},
        {"id": "03", "input": "5 100\n1 1 1 1 1\n"},
        {"id": "04", "input": "1 5\n5\n"},
        {"id": "05", "input": "2 3\n1 2\n"},
        {"id": "06", "input": "2000 2000\n" + " ".join(ones[:2000]) + "\n"},
        {"id": "07", "input": "200000 1\n" + " ".join(big) + "\n"},
        {"id": "08", "input": "200000 50000\n" + " ".join(mid) + "\n"},
        {"id": "09", "input": "200000 100000000000\n" + " ".join(wide) + "\n"},
        {"id": "10", "input": "200000 100000000000000\n" + " ".join(mid) + "\n"},
        {"id": "11", "input": "200000 2000000000\n" + " ".join(sparse) + "\n"},
        {"id": "12", "input": "200000 999999999\n" + " ".join(mixed) + "\n"},
    ]
