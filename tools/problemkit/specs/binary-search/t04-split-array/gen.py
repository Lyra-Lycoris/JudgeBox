import random


def pack(a, k):
    return "%d\n%s\n%d\n" % (len(a), " ".join(str(v) for v in a), k)


def cases():
    rng = random.Random(20261126)
    out = [{"id": "01", "input": pack([7, 2, 5, 10, 8], 2)}]
    out.append({"id": "02", "input": pack([9], 1)})
    out.append({"id": "03", "input": pack([5, 5, 5, 5, 5], 5)})
    out.append({"id": "04", "input": pack([0] * 10, 3)})
    out.append({"id": "05", "input": pack([1, 2, 3, 4, 5], 1)})
    out.append({"id": "06", "input": pack([0, 0, 7, 0, 0], 2)})
    out.append({"id": "07", "input": pack([rng.randint(0, 10 ** 6) for _ in range(1000)], 7)})

    n = 200000
    out.append({"id": "08", "input": pack([rng.randint(0, 10 ** 4) for _ in range(n)], 3)})
    out.append({"id": "09", "input": pack([10 ** 9] * n, n // 2)})
    out.append({"id": "10", "input": pack([rng.randint(0, 10 ** 9) for _ in range(n)], n - 1)})
    out.append({"id": "11", "input": pack([10 ** 9] * n, 1)})
    return out
