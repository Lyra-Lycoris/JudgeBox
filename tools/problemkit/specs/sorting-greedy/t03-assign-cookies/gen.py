import random


def pack(g, s):
    return "%d\n%s\n%d\n%s\n" % (len(g), " ".join(str(x) for x in g),
                                 len(s), " ".join(str(x) for x in s))


def cases():
    rng = random.Random(20260302)
    out = [{"id": "01", "input": pack([1, 2], [1, 2, 3])}]
    out.append({"id": "02", "input": pack([5], [3])})
    out.append({"id": "03", "input": pack([7, 7, 7, 7], [7, 7, 7, 7])})
    out.append({"id": "04", "input": pack([1000000000], [1000000000])})
    out.append({"id": "05", "input": pack([1, 2, 3, 4, 5], [10, 20])})
    out.append({"id": "06", "input": pack([1, 1, 1], [1000000000, 999999999, 1])})

    n = 3000
    g = [rng.randint(1, 1000) for _ in range(n)]
    s = [rng.randint(1, 1000) for _ in range(n)]
    out.append({"id": "07", "input": pack(g, s)})

    n = 100000
    g = [rng.randint(1, 10 ** 9) for _ in range(n)]
    s = [rng.randint(1, 10 ** 9) for _ in range(n)]
    out.append({"id": "08", "input": pack(g, s)})

    n = 100000
    g = [rng.randint(1, 1000) for _ in range(n)]
    s = [rng.randint(1, 10 ** 9) for _ in range(n)]
    out.append({"id": "09", "input": pack(g, s)})
    return out
