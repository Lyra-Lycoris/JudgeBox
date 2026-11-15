import random


def _pack(values):
    return "%d\n%s\n" % (len(values), " ".join(str(v) for v in values))


def _build(rng, pairs, first, last):
    values = []
    for p in pairs:
        values.append(p)
        values.append(p)
    values.append(first)
    values.append(last)
    rng.shuffle(values)
    return values


def cases():
    rng = random.Random(20261115)
    out = [
        {"id": "01", "input": "6\n1 2 1 3 2 5\n"},
        {"id": "02", "input": "2\n-4 9\n"},
        {"id": "03", "input": "2\n-1000000000 1000000000\n"},
        {"id": "04", "input": "4\n1 1 2 3\n"},
        {"id": "05", "input": "8\n5 3 5 7 3 7 1 9\n"},
        {"id": "06", "input": "8\n-1000000000 1000000000 -3 -3 -7 -7 15 15\n"},
    ]

    # 两个只出现一次的数共享高位：536870912 = 2^29，536870913 = 2^29 + 1
    pairs = rng.sample(range(-536870912, 0), 50)
    out.append({"id": "07", "input": _pack(_build(rng, pairs, 536870912, 536870913))})

    pairs = rng.sample(range(-10 ** 9, 0), 500)
    out.append({"id": "08", "input": _pack(_build(rng, pairs, 0, 1000000000))})

    pairs = [i * 7919 + 1 for i in range(99998)]
    out.append({"id": "09", "input": _pack(_build(rng, pairs, 0, 1000000000))})

    # 两个只出现一次的数都是负数：-1 与 -2
    pairs = rng.sample(range(-10 ** 9, -2), 99999)
    out.append({"id": "10", "input": _pack(_build(rng, pairs, -1, -2))})
    return out
