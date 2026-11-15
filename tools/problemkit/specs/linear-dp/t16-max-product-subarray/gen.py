import random


def _line(values):
    return " ".join(str(x) for x in values)


def _runs(rng, n, max_run, zero_prob):
    """连续非零段长度不超过 max_run，段之间插入 0。"""
    out = []
    run = 0
    while len(out) < n:
        if run >= max_run or (run > 0 and rng.random() < zero_prob):
            out.append(0)
            run = 0
        else:
            out.append(rng.choice((-2, -1, 1, 2)))
            run += 1
    return out


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "5\n2 -2 -1 0 1\n"},
        {"id": "02", "input": "1\n0\n"},
        {"id": "03", "input": "1\n-2\n"},
        {"id": "04", "input": "3\n-2 -1 -2\n"},
        {"id": "05", "input": "6\n0 0 0 0 0 0\n"},
        {"id": "06", "input": "10\n2 2 2 2 2 2 2 2 2 2\n"},
        {"id": "07", "input": "6\n2 -2 2 -2 2 -2\n"},
    ]

    def add(a):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d\n%s\n" % (len(a), _line(a))})

    add(_runs(rng, 1000, 40, 0.10))
    add(_runs(rng, 200000, 40, 0.05))

    block = [2] * 50 + [0]
    big = (block * ((200000 // len(block)) + 1))[:200000]
    add(big)

    sparse = [0] * 200000
    for start in range(0, 200000, 7777):
        for j in range(start, min(start + 30, 200000)):
            sparse[j] = rng.choice((-2, -1, 1, 2))
    add(sparse)
    return out
