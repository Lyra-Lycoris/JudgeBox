import random


def pack(n, w, p):
    lines = [str(n), " ".join(str(x) for x in w)]
    if p:
        lines.append(" ".join(str(x) for x in p))
    return "\n".join(lines) + "\n"


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
    out.append({"id": "01", "input": pack(6, [3, -2, 5, 4, -1, 2], [1, 1, 2, 2, 4])})
    out.append({"id": "02", "input": pack(1, [-5], [])})
    out.append({"id": "03", "input": pack(2, [7, 8], [1])})
    out.append({"id": "04", "input": pack(2, [-1, -2], [1])})
    out.append({"id": "05", "input": pack(10, list(range(1, 11)), path_parents(10))})
    out.append({"id": "06", "input": pack(9, [0, 0, 0, 0, 0, 0, 0, 0, 0], binary_parents(9))})
    out.append({"id": "07", "input": pack(1000, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(1000)],
                                          star_parents(1000))})
    out.append({"id": "08", "input": pack(5000, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(5000)],
                                          random_tree(rng, 5000))})
    n = 200000
    out.append({"id": "09", "input": pack(n, [(-1) ** i * (i % 1000) for i in range(n)], path_parents(n))})
    out.append({"id": "10", "input": pack(n, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)],
                                          random_tree(rng, n))})
    out.append({"id": "11", "input": pack(n, [5] * n, star_parents(n))})
    out.append({"id": "12", "input": pack(n, [-i % 1000 - 1 for i in range(n)], path_parents(n))})
    return out
