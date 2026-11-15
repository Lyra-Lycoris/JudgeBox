import random


def pack(n, l, r):
    return "%d\n%s\n%s\n" % (n, " ".join(str(x) for x in l), " ".join(str(x) for x in r))


def cases():
    rng = random.Random(20260301)
    out = [{"id": "01", "input": pack(4, [1, 2, 3, 0], [3, 4, 5, 1])}]
    out.append({"id": "02", "input": pack(1, [5], [7])})
    out.append({"id": "03", "input": pack(5, [2] * 5, [2] * 5)})
    out.append({"id": "04", "input": pack(4, [-10, -5, -1, -7], [-6, -4, 0, -3])})
    out.append({"id": "05", "input": pack(2, [0, 1000000000], [0, 1000000000])})

    n = 2000
    l, r = [], []
    for _ in range(n):
        a = rng.randint(-10 ** 9, 10 ** 9)
        b = min(10 ** 9, a + rng.randint(0, 10 ** 6))
        l.append(a)
        r.append(b)
    out.append({"id": "06", "input": pack(n, l, r)})

    n = 150000
    l, r = [], []
    for _ in range(n):
        a = rng.randint(-10 ** 9, 10 ** 9)
        b = min(10 ** 9, a + rng.randint(0, 10 ** 9))
        l.append(a)
        r.append(b)
    out.append({"id": "07", "input": pack(n, l, r)})

    n = 200000
    l = [rng.randint(0, 1000) for _ in range(n)]
    r = [x + rng.randint(0, 1000) for x in l]
    out.append({"id": "08", "input": pack(n, l, r)})
    return out
