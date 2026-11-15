import random


def pack(n, s, d):
    return "%d %d\n%s\n%s\n" % (n, len(s), " ".join(str(x) for x in s),
                                " ".join(str(x) for x in d))


def random_meetings(m, lo, hi, dlo, dhi, rng):
    s = [rng.randint(lo, hi) for _ in range(m)]
    d = [rng.randint(dlo, dhi) for _ in range(m)]
    return s, d


def cases():
    rng = random.Random(20260908)
    out = [{"id": "01", "input": pack(2, [0, 1, 2, 3], [10, 4, 5, 1])}]
    out.append({"id": "02", "input": pack(1, [5], [7])})
    out.append({"id": "03", "input": pack(2, [0, 0, 0, 0], [1, 1, 1, 1])})
    out.append({"id": "04", "input": pack(3, [0, 10, 20], [5, 5, 5])})
    out.append({"id": "05", "input": pack(1, [0, 0, 0], [1000000000, 1000000000, 1000000000])})
    out.append({"id": "06", "input": pack(3, [0, 1000000000, 999999999, 0, 500000000],
                                         [1000000000, 1000000000, 1, 1, 1000000000])})

    s, d = random_meetings(2000, 0, 10 ** 6, 1, 1000, rng)
    out.append({"id": "07", "input": pack(50, s, d)})

    s, d = random_meetings(200000, 0, 10 ** 9, 1, 10, rng)
    out.append({"id": "08", "input": pack(100000, s, d)})

    s = [0] * 200000
    d = [rng.randint(1, 10 ** 9) for _ in range(200000)]
    out.append({"id": "09", "input": pack(1, s, d)})

    s, d = random_meetings(200000, 0, 1000, 1, 10 ** 6, rng)
    out.append({"id": "10", "input": pack(100, s, d)})
    return out
