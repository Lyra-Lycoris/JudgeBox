import random


def pack(a, k):
    return "%d\n%s\n%d\n" % (len(a), " ".join(str(x) for x in a), k)


def cases():
    rng = random.Random(20260308)
    out = [{"id": "01", "input": pack([1, 5, 3, 9, 11], 3)}]
    out.append({"id": "02", "input": pack([7], 1)})
    out.append({"id": "03", "input": pack([5, 5, 5, 5, 5], 3)})
    out.append({"id": "04", "input": pack([1, 2, 4, 8], 4)})
    out.append({"id": "05", "input": pack([-10, -3, -3, 0, 5, 1000000000], 3)})
    out.append({"id": "06", "input": pack([-1000000000, 1000000000], 2)})

    n = 3000
    out.append({"id": "07", "input": pack([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)], 50)})

    n = 100000
    out.append({"id": "08", "input": pack([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)], 3)})

    n = 100000
    out.append({"id": "09", "input": pack([i * 10000 for i in range(n)], 50000)})
    return out
