import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "6\n7 1 5 3 6 4\n"},
        {"id": "02", "input": "1\n5\n"},
        {"id": "03", "input": "5\n5 4 3 2 1\n"},
        {"id": "04", "input": "5\n1 2 3 4 5\n"},
        {"id": "05", "input": "4\n3 3 3 3\n"},
        {"id": "06", "input": "8\n3 3 5 0 0 3 1 4\n"},
    ]

    def add(a):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d\n%s\n" % (len(a), _line(a))})

    add([rng.randint(0, 1000000000) for _ in range(1000)])

    n = 200000
    add([rng.randint(0, 1000000000) for _ in range(n)])
    add([1000000000 - i * 5000 for i in range(n)])
    add([i * 5000 for i in range(n)])
    add([1000000000 - i * 5000 for i in range(n // 2)] + [i * 5000 for i in range(n // 2)])
    return out
