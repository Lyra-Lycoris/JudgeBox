import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261123)
    out = [
        {"id": "01", "input": "9\n-2 1 -3 4 -1 2 1 -5 4\n"},
        {"id": "02", "input": "5\n-3 -1 -7 -2 -5\n"},
        {"id": "03", "input": "1\n-1000000000\n"},
        {"id": "04", "input": "2\n-1 -2\n"},
        {"id": "05", "input": "6\n1 2 3 4 5 6\n"},
        {"id": "06", "input": "12\n4 -5 4 -5 4 -5 4 -5 4 -5 4 -5\n"},
    ]

    def add(a):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d\n%s\n" % (len(a), _line(a))})

    add([rng.randint(-1000, 1000) for _ in range(1000)])

    n = 200000
    add([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)])
    add([-10 ** 9] * n)
    add([10 ** 9] * n)
    add([rng.randint(-10 ** 9, 0) for _ in range(n // 2)] + [10 ** 9] +
        [rng.randint(-10 ** 9, 0) for _ in range(n // 2 - 1)])
    return out
