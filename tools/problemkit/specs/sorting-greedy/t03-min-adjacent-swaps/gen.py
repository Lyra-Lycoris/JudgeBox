import random


def pack(a):
    return "%d\n%s\n" % (len(a), " ".join(str(x) for x in a))


def cases():
    rng = random.Random(20260306)
    out = [{"id": "01", "input": pack([2, 4, 1, 3])}]
    out.append({"id": "02", "input": pack([-5])})
    out.append({"id": "03", "input": pack([5, 5, 5, 5])})
    out.append({"id": "04", "input": pack([5, 4, 3, 2, 1])})
    out.append({"id": "05", "input": pack([-3, 5, -3, 0, 5, -3, 1000000000, -1000000000])})
    out.append({"id": "06", "input": pack([0, 0, 1, 0, 0, 1, 1, 0])})

    n = 3000
    out.append({"id": "07", "input": pack([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)])})

    n = 100000
    out.append({"id": "08", "input": pack([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)])})

    n = 100000
    out.append({"id": "09", "input": pack(list(range(n, 0, -1)))})
    return out
