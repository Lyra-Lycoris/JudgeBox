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


def caterpillar(rng, n):
    # 一条一半长度的脊，每个脊节点再挂一片叶子
    spine = n // 2
    p = []
    for i in range(2, spine + 1):
        p.append(i - 1)
    for i in range(spine + 1, n + 1):
        p.append(rng.randint(1, spine))
    return p


def cases():
    rng = random.Random(20261117)
    out = []
    out.append({"id": "01", "input": pack(5, [1, 1, 3, 3])})
    out.append({"id": "02", "input": pack(1, [])})
    out.append({"id": "03", "input": pack(2, [1])})
    out.append({"id": "04", "input": pack(6, path_parents(6))})
    out.append({"id": "05", "input": pack(7, star_parents(7))})
    out.append({"id": "06", "input": pack(1000, random_tree(rng, 1000))})
    n = 200000
    out.append({"id": "07", "input": pack(n, path_parents(n))})
    out.append({"id": "08", "input": pack(n, star_parents(n))})
    out.append({"id": "09", "input": pack(n, random_tree(rng, n))})
    out.append({"id": "10", "input": pack(n, binary_parents(n))})
    out.append({"id": "11", "input": pack(n, caterpillar(rng, n))})
    return out
