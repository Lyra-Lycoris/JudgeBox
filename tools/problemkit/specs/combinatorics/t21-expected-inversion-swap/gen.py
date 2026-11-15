import random


def join(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261122)
    n = 200000
    increasing = list(range(1, n + 1))
    decreasing = list(range(n, 0, -1))
    wide = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    small = [rng.randint(0, 3) for _ in range(n)]
    medium = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(2000)]
    return [
        {"id": "01", "input": "3\n3 1 2\n"},
        {"id": "02", "input": "1\n5\n"},
        {"id": "03", "input": "2\n1 2\n"},
        {"id": "04", "input": "2\n2 1\n"},
        {"id": "05", "input": "4\n4 3 2 1\n"},
        {"id": "06", "input": "4\n1 1 1 1\n"},
        {"id": "07", "input": "200000\n" + join([0] * n) + "\n"},
        {"id": "08", "input": "200000\n" + join(increasing) + "\n"},
        {"id": "09", "input": "200000\n" + join(decreasing) + "\n"},
        {"id": "10", "input": "200000\n" + join(wide) + "\n"},
        {"id": "11", "input": "200000\n" + join(small) + "\n"},
        {"id": "12", "input": "2000\n" + join(medium) + "\n"},
    ]
