import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261121)
    out = [
        {"id": "01", "input": "6\n2 3 4 5 6 1\n"},
        {"id": "02", "input": "1\n-7\n"},
        {"id": "03", "input": "5\n3 3 3 3 3\n"},
        {"id": "04", "input": "6\n1 2 3 4 5 6\n"},
        {"id": "05", "input": "6\n6 5 4 3 2 1\n"},
        {"id": "06", "input": "7\n-2 5 -9 0 5 -9 7\n"},
    ]

    def add(a):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d\n%s\n" % (len(a), _line(a))})

    add([rng.randint(-10 ** 9, 10 ** 9) for _ in range(1000)])

    n = 200000
    add([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)])
    add([0] * n)
    add(list(range(n, 0, -1)))

    nearly = list(range(1, n + 1))
    for _ in range(50):
        i = rng.randrange(n)
        j = rng.randrange(n)
        nearly[i], nearly[j] = nearly[j], nearly[i]
    add(nearly)
    return out
