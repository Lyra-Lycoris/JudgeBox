import random


def join(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261121)
    n = 200000
    all_same = [7] * n
    distinct = list(range(1, n + 1))
    thousands = [rng.randint(0, 999) for _ in range(n)]
    wide = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    medium = [rng.randint(0, 999) for _ in range(1000)]
    mixed = [rng.choice([0, 0, 1, 5, 5, 5, -10 ** 9, 10 ** 9]) for _ in range(12345)]
    return [
        {"id": "01", "input": "3\n1 1 2\n"},
        {"id": "02", "input": "1\n-5\n"},
        {"id": "03", "input": "2\n7 7\n"},
        {"id": "04", "input": "5\n1 2 3 4 5\n"},
        {"id": "05", "input": "4\n2 2 2 2\n"},
        {"id": "06", "input": "6\n1 1 2 2 3 3\n"},
        {"id": "07", "input": "200000\n" + join(all_same) + "\n"},
        {"id": "08", "input": "200000\n" + join(distinct) + "\n"},
        {"id": "09", "input": "200000\n" + join(thousands) + "\n"},
        {"id": "10", "input": "200000\n" + join(wide) + "\n"},
        {"id": "11", "input": "1000\n" + join(medium) + "\n"},
        {"id": "12", "input": "12345\n" + join(mixed) + "\n"},
    ]
