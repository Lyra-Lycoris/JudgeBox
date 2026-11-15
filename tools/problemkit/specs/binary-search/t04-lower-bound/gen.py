import random


def pack(a, x):
    return "%d\n%s\n%d\n" % (len(a), " ".join(str(v) for v in a), x)


def cases():
    rng = random.Random(20261121)
    out = [{"id": "01", "input": pack([1, 3, 5, 7, 9], 5)}]
    out.append({"id": "02", "input": pack([7], 7)})
    out.append({"id": "03", "input": pack([7], 8)})
    out.append({"id": "04", "input": pack([4, 4, 4, 4, 4, 4], 5)})
    out.append({"id": "05", "input": pack([4] * 8, 4)})
    out.append({"id": "06", "input": pack([-9, -5, -5, -1, 0, 3], -5)})
    out.append({"id": "07", "input": pack([-3, -1, 2], -1000000000)})
    out.append({"id": "08", "input": pack([-3, -1, 2], 1000000000)})

    n = 1000
    a = sorted(rng.randint(-1000, 1000) for _ in range(n))
    out.append({"id": "09", "input": pack(a, rng.randint(-1000, 1000))})

    n = 200000
    a = sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(n))
    out.append({"id": "10", "input": pack(a, rng.randint(-10 ** 9, 10 ** 9))})
    out.append({"id": "11", "input": pack([-1000000000] * 50000 + [1000000000] * 50000, 1000000000)})
    return out
