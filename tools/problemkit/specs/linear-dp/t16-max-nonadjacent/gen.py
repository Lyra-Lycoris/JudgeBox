import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "5\n2 7 9 3 1\n"},
        {"id": "02", "input": "1\n5\n"},
        {"id": "03", "input": "2\n1 2\n"},
        {"id": "04", "input": "3\n2 1 1\n"},
        {"id": "05", "input": "6\n7 7 7 7 7 7\n"},
        {"id": "06", "input": "5\n0 0 0 0 0\n"},
        {"id": "07", "input": "10\n100 1 100 1 100 1 100 1 100 1\n"},
    ]

    def add(a):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d\n%s\n" % (len(a), _line(a))})

    add([rng.randint(0, 1000000000) for _ in range(1000)])

    n = 200000
    add([rng.randint(0, 1000000000) for _ in range(n)])
    add([1000000000] * n)
    add([(i * 7919) % 2 * 1000000000 for i in range(n)])
    return out
