import random


def cases():
    rng = random.Random(20261119)
    n = 200000
    alt = [1 if i % 2 == 0 else 0 for i in range(n)]
    block = [1, 1, 1, 0] * (n // 4)
    mid7 = [0, 0, 1, 1, 1, 0, 0]
    return [
        {"id": "01", "input": "4\n1 1 0 1\n"},
        {"id": "02", "input": "5\n1 0 1 0 1\n"},
        {"id": "03", "input": "7\n" + " ".join(str(x) for x in mid7) + "\n"},
        {"id": "04", "input": "1\n1\n"},
        {"id": "05", "input": "1\n0\n"},
        {"id": "06", "input": "200000\n" + " ".join(["1"] * n) + "\n"},
        {"id": "07", "input": "200000\n" + " ".join(["0"] * n) + "\n"},
        {"id": "08", "input": "200000\n" + " ".join(str(x) for x in alt) + "\n"},
        {"id": "09", "input": "200000\n" + " ".join(str(x) for x in block) + "\n"},
        {"id": "10", "input": "2000\n" + " ".join(str(1 if rng.random() < 0.7 else 0) for _ in range(2000)) + "\n"},
        {"id": "11", "input": "200000\n" + " ".join(str(1 if rng.random() < 0.5 else 0) for _ in range(n)) + "\n"},
        {"id": "12", "input": "200000\n" + " ".join(str(1 if rng.random() < 0.95 else 0) for _ in range(n)) + "\n"},
    ]
