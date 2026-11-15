import random


def pack(a, k):
    return "%d\n%s\n%d\n" % (len(a), " ".join(str(v) for v in a), k)


def cases():
    rng = random.Random(20261122)
    out = [{"id": "01", "input": pack([8, 7, 6, 5], 4)}]
    out.append({"id": "02", "input": pack([1], 1)})
    out.append({"id": "03", "input": pack([5], 6)})
    out.append({"id": "04", "input": pack([1000000000] * 3, 1000000000)})
    out.append({"id": "05", "input": pack([3, 1, 4, 1, 5], 1)})
    out.append({"id": "06", "input": pack([3, 3, 3], 9)})
    out.append({"id": "07", "input": pack([rng.randint(1, 10 ** 6) for _ in range(2000)], 10 ** 6)})

    n = 200000
    out.append({"id": "08", "input": pack([rng.randint(1, 10 ** 9) for _ in range(n)], 10 ** 9)})
    out.append({"id": "09", "input": pack([10 ** 9] * n, 1)})
    out.append({"id": "10", "input": pack([1] * n, n)})
    return out
