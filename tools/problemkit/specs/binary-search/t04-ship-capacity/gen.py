import random


def pack(w, d):
    return "%d\n%s\n%d\n" % (len(w), " ".join(str(v) for v in w), d)


def cases():
    rng = random.Random(20261123)
    out = [{"id": "01", "input": pack(list(range(1, 11)), 5)}]
    out.append({"id": "02", "input": pack([5], 1)})
    out.append({"id": "03", "input": pack([3, 1, 4, 1, 5], 5)})
    out.append({"id": "04", "input": pack([1, 2, 3], 1)})
    out.append({"id": "05", "input": pack([7] * 1000, 3)})
    out.append({"id": "06", "input": pack([10 ** 9] * 3, 2)})
    out.append({"id": "07", "input": pack([rng.randint(1, 10 ** 4) for _ in range(5000)], 50)})

    n = 200000
    out.append({"id": "08", "input": pack([rng.randint(1, 1000) for _ in range(n)], 1000)})
    out.append({"id": "09", "input": pack([10 ** 9] * n, n // 2)})
    out.append({"id": "10", "input": pack([rng.randint(1, 10 ** 9) for _ in range(n)], 1)})
    return out
