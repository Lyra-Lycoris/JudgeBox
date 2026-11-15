import random


def pack(l, r, m):
    return "%d\n%s\n%s\n%d\n" % (len(l), " ".join(str(x) for x in l),
                                 " ".join(str(x) for x in r), m)


def chain(rng, m, segs):
    cuts = sorted(rng.sample(range(1, m), segs - 1))
    pts = [0] + cuts + [m]
    return [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


def cases():
    rng = random.Random(20260307)
    out = [{"id": "01", "input": pack([0, 2, 4], [3, 6, 8], 6)}]
    out.append({"id": "02", "input": pack([0, 1], [1, 2], 2)})
    out.append({"id": "03", "input": pack([0, 1], [1, 2], 5)})
    out.append({"id": "04", "input": pack([-5], [10], 10)})
    out.append({"id": "05", "input": pack([-10, -2, 4], [3, 8, 8], 8)})

    m = 1000000
    l, r = [], []
    for a, b in chain(rng, m, 500):
        l.append(a)
        r.append(b)
    for _ in range(500):
        a = rng.randint(0, m - 1)
        l.append(a)
        r.append(rng.randint(a, m))
    out.append({"id": "06", "input": pack(l, r, m)})

    m = 10 ** 9
    l, r = [], []
    for a, b in chain(rng, m, 100000):
        l.append(a)
        r.append(b)
    out.append({"id": "07", "input": pack(l, r, m)})

    m = 10 ** 9
    l = [i * 10000 for i in range(100000)]
    r = [(i + 1) * 10000 for i in range(100000)]
    out.append({"id": "08", "input": pack(l, r, m)})
    return out
