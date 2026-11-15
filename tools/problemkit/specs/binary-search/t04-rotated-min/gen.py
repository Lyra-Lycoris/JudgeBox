import random


def pack(a):
    return "%d\n%s\n" % (len(a), " ".join(str(v) for v in a))


def rotate(b, shift):
    k = shift % len(b)
    return b[k:] + b[:k]


def cases():
    rng = random.Random(20261124)
    out = [{"id": "01", "input": pack([4, 5, 6, 7, 0, 1, 2])}]
    out.append({"id": "02", "input": pack([5])})
    out.append({"id": "03", "input": pack([1, 2, 3, 4, 5])})
    out.append({"id": "04", "input": pack([2, 3, 4, 5, 1])})
    out.append({"id": "05", "input": pack([3, 5, -9, -5, -1, 0])})
    out.append({"id": "06", "input": pack([2, 1])})
    out.append({"id": "07", "input": pack([3, 1, 2])})

    n = 1000
    base = sorted(rng.sample(range(-10000, 10000), n))
    out.append({"id": "08", "input": pack(rotate(base, rng.randrange(n)))})

    n = 200000
    base = sorted(rng.sample(range(-10 ** 9, 10 ** 9), n))
    out.append({"id": "09", "input": pack(rotate(base, rng.randrange(n)))})
    out.append({"id": "10", "input": pack(rotate(base, n - 1))})

    base = list(range(-1000000000, -1000000000 + 7))
    out.append({"id": "11", "input": pack(rotate(base, 3))})
    return out
