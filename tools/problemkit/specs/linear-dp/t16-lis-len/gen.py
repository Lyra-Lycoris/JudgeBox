import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "8\n10 9 2 5 3 7 101 18\n"},
        {"id": "02", "input": "1\n5\n"},
        {"id": "03", "input": "8\n8 7 6 5 4 3 2 1\n"},
        {"id": "04", "input": "6\n3 3 3 3 3 3\n"},
        {"id": "05", "input": "10\n1 2 3 4 5 6 7 8 9 10\n"},
        {"id": "06", "input": "7\n2 2 3 3 4 4 5\n"},
    ]

    def add(a):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d\n%s\n" % (len(a), _line(a))})

    perm = list(range(1, 1001))
    rng.shuffle(perm)
    add(perm)

    add([rng.randint(1, 10) for _ in range(2000)])

    n = 200000
    add([rng.randint(-1000000000, 1000000000) for _ in range(n)])
    add(list(range(1, n + 1)))
    add(list(range(1, n // 2 + 1)) + list(range(n // 2, 0, -1)))

    saw = []
    for i in range(n):
        saw.append(1 if i % 2 == 0 else 1000000000)
    add(saw)
    return out
