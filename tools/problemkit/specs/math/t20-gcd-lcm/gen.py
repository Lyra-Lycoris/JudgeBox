import random


def pack(pairs):
    return "%d\n%s" % (len(pairs), "\n".join("%d %d" % (a, b) for a, b in pairs))


def cases():
    rng = random.Random(20261114)
    out = []
    out.append({"id": "01", "input": pack([(12, 18), (7, 5), (1000000000, 999999999)])})
    out.append({"id": "02", "input": pack([(1, 1)])})
    out.append({"id": "03", "input": pack([(0, 5), (0, 0), (5, 0)])})
    out.append({"id": "04", "input": pack([(1000000000, 1000000000), (999999999, 999999999)])})
    out.append({"id": "05", "input": pack([(1, 1000000000), (1000000000, 1), (999999937, 1000000000)])})
    out.append({"id": "06", "input": pack([(12, 18), (18, 12), (100, 75), (756, 432)])})
    out.append({"id": "07", "input": pack([(rng.randint(1, 10 ** 9), rng.randint(1, 10 ** 9)) for _ in range(500)])})
    out.append({"id": "08", "input": pack([(rng.randint(0, 10 ** 9), rng.randint(0, 10 ** 9)) for _ in range(1000)])})
    out.append({"id": "09", "input": pack([(rng.randint(1, 100), rng.randint(1, 100)) for _ in range(1000)])})
    return out
