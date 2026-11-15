import random


def pack(k, a):
    return "%d %d\n%s\n" % (len(a), k, " ".join(str(x) for x in a))


def cases():
    rng = random.Random(20260901)
    out = [{"id": "01", "input": "6 2\n3 2 1 5 6 4\n"}]
    out.append({"id": "02", "input": pack(1, [-7])})
    out.append({"id": "03", "input": pack(4, [5] * 7)})
    out.append({"id": "04", "input": pack(5, [-1, -2, -3, -4, -5])})
    out.append({"id": "05", "input": pack(1, [1000000000, -1000000000, 999999999, -999999999, 0, 7])})
    out.append({"id": "06", "input": pack(8, [3, 1, 4, 1, 5, 9, 2, 6])})

    n = 2000
    out.append({"id": "07", "input": pack(777, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)])})

    n = 200000
    out.append({"id": "08", "input": pack(100000, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)])})

    out.append({"id": "09", "input": pack(1, [0] * 200000)})
    return out
