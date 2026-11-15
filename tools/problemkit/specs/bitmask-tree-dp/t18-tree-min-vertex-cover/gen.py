import random


def pack(n, p):
    if not p:
        return "%d\n" % n
    return "%d\n%s\n" % (n, " ".join(str(x) for x in p))


def path_parents(n):
    return [i - 1 for i in range(2, n + 1)]


def star_parents(n):
    return [1] * (n - 1)


def binary_parents(n):
    return [i // 2 for i in range(2, n + 1)]


def random_tree(rng, n):
    return [rng.randint(1, i - 1) for i in range(2, n + 1)]


def cases():
    rng = random.Random(20261114)
    out = []
    out.append({"id": "01", "input": pack(5, [1, 1, 3, 3])})
    out.append({"id": "02", "input": pack(1, [])})
    out.append({"id": "03", "input": pack(2, [1])})
    out.append({"id": "04", "input": pack(7, path_parents(7))})
    out.append({"id": "05", "input": pack(8, star_parents(8))})
    out.append({"id": "06", "input": pack(15, binary_parents(15))})
    out.append({"id": "07", "input": pack(1000, random_tree(rng, 1000))})
    out.append({"id": "08", "input": pack(200000, path_parents(200000))})
    out.append({"id": "09", "input": pack(200000, star_parents(200000))})
    out.append({"id": "10", "input": pack(200000, random_tree(rng, 200000))})
    out.append({"id": "11", "input": pack(200000, binary_parents(200000))})
    return out
