import random


def pack(k, a):
    return "%d %d\n%s\n" % (len(a), k, " ".join(str(x) for x in a))


def cases():
    rng = random.Random(20260907)
    out = [{"id": "01", "input": pack(2, [1, 1, 1, 2, 2, 3])}]
    out.append({"id": "02", "input": pack(1, [-5])})
    out.append({"id": "03", "input": pack(1, [9] * 10)})
    out.append({"id": "04", "input": pack(2, [3, 3, -1, -1, 7, 7])})
    out.append({"id": "05", "input": pack(5, [5, 4, 3, 2, 1])})
    out.append({"id": "06", "input": pack(2, [1000000000, -1000000000, 1000000000,
                                             -1000000000, 7])})

    out.append({"id": "07", "input": pack(20, [rng.randint(0, 50) for _ in range(2000)])})
    out.append({"id": "08", "input": pack(100000, [rng.randint(0, 10 ** 9) for _ in range(200000)])})

    stacked = [i % 101 for i in range(200000)]
    rng.shuffle(stacked)
    out.append({"id": "09", "input": pack(101, stacked)})
    return out
