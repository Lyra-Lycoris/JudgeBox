import random


def pack(a):
    return "%d\n%s\n" % (len(a), " ".join(str(v) for v in a))


def cases():
    rng = random.Random(20261125)
    out = [{"id": "01", "input": pack([1, 2, 3, 0])}]
    out.append({"id": "02", "input": pack([5])})
    out.append({"id": "03", "input": pack([1, 2, 3, 4, 5])})
    out.append({"id": "04", "input": pack([5, 4, 3, 2, 1])})
    out.append({"id": "05", "input": pack([-3, -1, -2, -5])})
    out.append({"id": "06", "input": pack([3, 1, 2])})

    n = 1000
    out.append({"id": "07", "input": pack(rng.sample(range(-10 ** 6, 10 ** 6), n))})

    n = 200000
    out.append({"id": "08", "input": pack(rng.sample(range(-10 ** 9, 10 ** 9), n))})
    out.append({"id": "09", "input": pack(list(range(1, n + 1)))})
    out.append({"id": "10", "input": pack(list(range(n, 0, -1)))})

    zigzag = []
    for i in range(n):
        if i % 2 == 0:
            zigzag.append(1000000 - i)
        else:
            zigzag.append(-1000000 + i)
    out.append({"id": "11", "input": pack(zigzag)})
    return out
