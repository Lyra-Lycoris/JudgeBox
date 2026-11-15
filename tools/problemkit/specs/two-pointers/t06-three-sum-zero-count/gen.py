import random


def cases():
    rng = random.Random(20261118)
    big_dense = [rng.randint(-1000, 1000) for _ in range(2000)]
    tiny_dense = [rng.randint(-5, 5) for _ in range(2000)]
    ladder = [i - 1000 for i in range(2000)]
    antisym = [0]
    for v in range(1, 1000):
        antisym.append(v)
        antisym.append(-v)
    mid = [rng.randint(-50, 50) for _ in range(100)]
    return [
        {"id": "01", "input": "6\n-1 0 1 2 -1 -4\n"},
        {"id": "02", "input": "5\n0 0 0 0 0\n"},
        {"id": "03", "input": "4\n1 2 3 4\n"},
        {"id": "04", "input": "1\n0\n"},
        {"id": "05", "input": "2\n1 -1\n"},
        {"id": "06", "input": "4\n-1 -1 2 0\n"},
        {"id": "07", "input": "100\n" + " ".join(str(x) for x in mid) + "\n"},
        {"id": "08", "input": "2000\n" + " ".join(str(x) for x in big_dense) + "\n"},
        {"id": "09", "input": "2000\n" + " ".join(["0"] * 2000) + "\n"},
        {"id": "10", "input": "2000\n" + " ".join(str(x) for x in tiny_dense) + "\n"},
        {"id": "11", "input": "2000\n" + " ".join(str(x) for x in ladder) + "\n"},
        {"id": "12", "input": "%d\n" % len(antisym) + " ".join(str(x) for x in antisym) + "\n"},
    ]
