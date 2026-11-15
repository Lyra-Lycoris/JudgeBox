import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261124)
    out = [
        {"id": "01", "input": "2\n1 3\n1\n2\n"},
        {"id": "02", "input": "2\n1 2\n2\n3 4\n"},
        {"id": "03", "input": "1\n-5\n1\n5\n"},
        {"id": "04", "input": "1\n0\n1\n0\n"},
        {"id": "05", "input": "3\n0 0 0\n3\n0 0 0\n"},
        {"id": "06", "input": "1\n-1000000000\n1\n1000000000\n"},
        {"id": "07", "input": "5\n-9 -4 0 3 7\n5\n-6 -2 1 5 8\n"},
    ]

    def add(a, b):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d\n%s\n%d\n%s\n" % (len(a), _line(a), len(b), _line(b))})

    add(sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(1000)),
        sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(1000)))

    n = 100000
    add(sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)),
        sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)))
    add(sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)),
        sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(1)))
    add(sorted(rng.randint(0, 10 ** 9) for _ in range(1)),
        sorted(rng.randint(0, 10 ** 9) for _ in range(n)))
    add([-10 ** 9] * n, [10 ** 9] * n)
    return out
