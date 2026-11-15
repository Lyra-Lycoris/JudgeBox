import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261125)
    out = [
        {"id": "01", "input": "3 1\n2 1 3\n"},
        {"id": "02", "input": "3 0\n5 5 5\n"},
        {"id": "03", "input": "3 2\n3 2 1\n"},
        {"id": "04", "input": "1 1\n5\n"},
        {"id": "05", "input": "1 0\n5\n"},
        {"id": "06", "input": "6 1\n4 4 4 4 4 4\n"},
        {"id": "07", "input": "6 15\n6 5 4 3 2 1\n"},
        {"id": "08", "input": "10 10000000000\n1 2 3 4 5 6 7 8 9 10\n"},
    ]

    def add(a, k):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d %d\n%s\n" % (len(a), k, _line(a))})

    add([rng.randint(-10 ** 9, 10 ** 9) for _ in range(300)], 50)

    n = 100000
    add([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)], 1000000)
    add(list(range(n, 0, -1)), 10 ** 9)
    add([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)], 0)
    return out
