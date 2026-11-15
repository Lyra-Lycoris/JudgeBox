import random
from collections import Counter


def line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261122)
    out = []

    def add(vals, cnts):
        total = Counter()
        for x, y in zip(vals, cnts):
            total[x] += y
        length = sum(cnts)
        assert max(total.values()) * 2 > length, (vals, cnts)
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d\n%s\n%s\n" % (len(vals), line(vals), line(cnts))})

    add([1, 2, 1, 3], [2, 1, 3, 1])
    add([0], [1])
    add([1000000000], [1000000000])
    add([5, 6, 5], [1, 1, 1])
    add([7, 8], [2, 1])
    add([8, 7], [1, 2])
    add([1, 2, 1, 2, 1], [1, 1, 1, 1, 1])
    add([1, 2, 3, 4, 5], [100, 1, 1, 1, 1])
    add([1, 2, 1], [1000000000, 999999999, 1000000000])

    n = 200000
    vals = [1 if i % 2 == 0 else 2 for i in range(n)]
    vals[-1] = 1
    add(vals, [1] * n)

    vals = [1 if i < 100001 else 2 for i in range(n)]
    add(vals, [1000000000] * n)

    vals = [2] * 100000 + [1] * 100000
    vals[0] = 1
    add(vals, [rng.randint(1, 1000) for _ in range(n)])
    return out
