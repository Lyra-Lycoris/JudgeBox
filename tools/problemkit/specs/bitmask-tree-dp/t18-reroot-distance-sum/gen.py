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
    out.append({"id": "04", "input": pack(5, path_parents(5))})
    out.append({"id": "05", "input": pack(6, star_parents(6))})
    out.append({"id": "06", "input": pack(1000, random_tree(rng, 1000))})
    n = 200000
    out.append({"id": "07", "input": pack(n, path_parents(n))})
    out.append({"id": "08", "input": pack(n, star_parents(n))})
    out.append({"id": "09", "input": pack(n, random_tree(rng, n))})
    out.append({"id": "10", "input": pack(n, binary_parents(n))})
    return out
