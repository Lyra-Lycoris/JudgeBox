import random


def pack(n, k, w, p):
    lines = ["%d %d" % (n, k), " ".join(str(x) for x in w)]
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
    out.append({"id": "01", "input": pack(6, 3, [4, -1, 7, 2, 5, -3], [1, 1, 2, 3, 3])})
    out.append({"id": "02", "input": pack(1, 1, [-7], [])})
    out.append({"id": "03", "input": pack(2, 1, [-3, 9], [1])})
    out.append({"id": "04", "input": pack(2, 2, [-3, 9], [1])})
    out.append({"id": "05", "input": pack(5, 3, [1, -2, 3, -4, 5], path_parents(5))})
    out.append({"id": "06", "input": pack(6, 4, [2, 6, -5, 8, -1, 3], star_parents(6))})
    out.append({"id": "07", "input": pack(100, 8, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(100)],
                                          random_tree(rng, 100))})
    out.append({"id": "08", "input": pack(1000, 20, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(1000)],
                                          random_tree(rng, 1000))})
    n = 3000
    out.append({"id": "09", "input": pack(n, 200, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)],
                                          path_parents(n))})
    out.append({"id": "10", "input": pack(n, 200, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)],
                                          star_parents(n))})
    out.append({"id": "11", "input": pack(n, 200, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)],
                                          binary_parents(n))})
    out.append({"id": "12", "input": pack(n, 150, [0] * n, random_tree(rng, n))})
    return out
