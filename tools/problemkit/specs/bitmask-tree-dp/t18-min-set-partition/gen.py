import random


def pack(n, c):
    return "%d\n%d\n%s\n" % (n, len(c), " ".join(str(x) for x in c))


def random_table(rng, n, hi):
    c = [0] * (1 << n)
    for s in range(1, 1 << n):
        c[s] = rng.randint(0, hi)
    return c


def cases():
    rng = random.Random(20261114)
    out = []
    out.append({"id": "01", "input": pack(3, [0, 5, 6, 4, 7, 3, 9, 10])})
    out.append({"id": "02", "input": pack(1, [0, 7])})
    out.append({"id": "03", "input": pack(2, [0, 4, 9, 6])})
    out.append({"id": "04", "input": pack(4, random_table(rng, 4, 20))})
    out.append({"id": "05", "input": pack(6, [0] * 64)})
    out.append({"id": "06", "input": pack(8, random_table(rng, 8, 10 ** 9))})
    out.append({"id": "07", "input": pack(10, random_table(rng, 10, 10 ** 9))})
    out.append({"id": "08", "input": pack(12, random_table(rng, 12, 10 ** 9))})
    out.append({"id": "09", "input": pack(15, [0] + [bin(s).count("1") for s in range(1, 1 << 15)])})
    out.append({"id": "10", "input": pack(15, [0] + [10 ** 9] * ((1 << 15) - 1))})
    out.append({"id": "11", "input": pack(15, random_table(rng, 15, 10 ** 9))})
    return out
