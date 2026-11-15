import random


def pack(n, w, edges, queries):
    parts = ["%d" % n, " ".join(str(x) for x in w)]
    parts += ["%d %d" % (u, v) for u, v in edges]
    parts.append("%d" % len(queries))
    parts += ["%d %d" % (a, b) for a, b in queries]
    return "\n".join(parts) + "\n"


def path_edges(n):
    return [(i, i + 1) for i in range(1, n)]


def star_edges(n):
    return [(1, i) for i in range(2, n + 1)]


def random_tree(rng, n):
    return [(rng.randint(1, i - 1), i) for i in range(2, n + 1)]


def random_pairs(rng, q, n):
    return [(rng.randint(1, n), rng.randint(1, n)) for _ in range(q)]


def cases():
    rng = random.Random(20261118)
    out = []
    out.append({"id": "01", "input": pack(
        5, [3, -1, 4, 1, 5],
        [(1, 2), (2, 3), (2, 4), (4, 5)],
        [(3, 5), (1, 5), (1, 1)])})
    out.append({"id": "02", "input": pack(1, [-5], [], [(1, 1)])})
    out.append({"id": "03", "input": pack(
        2, [1000000000, -1000000000], [(1, 2)], [(1, 2), (2, 2), (1, 1)])})
    out.append({"id": "04", "input": pack(
        10, [i * 7 - 40 for i in range(1, 11)], path_edges(10),
        [(1, 10), (10, 1), (3, 8), (5, 5)])})
    out.append({"id": "05", "input": pack(
        8, [-1000000000, 1000000000, -1, 1, 0, 5, -5, 2], star_edges(8),
        [(2, 3), (4, 8), (1, 5), (6, 7)])})
    out.append({"id": "06", "input": pack(
        100, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(100)],
        random_tree(rng, 100), random_pairs(rng, 100, 100))})
    out.append({"id": "07", "input": pack(
        5000, [rng.randint(-1000, 1000) for _ in range(5000)],
        random_tree(rng, 5000), random_pairs(rng, 5000, 5000))})
    out.append({"id": "08", "input": pack(
        100000, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(100000)],
        path_edges(100000), random_pairs(rng, 100000, 100000))})
    out.append({"id": "09", "input": pack(
        100000, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(100000)],
        random_tree(rng, 100000), random_pairs(rng, 100000, 100000))})
    out.append({"id": "10", "input": pack(
        150000, [1000000000] * 150000, path_edges(150000),
        [(1, 150000), (75000, 75000), (1, 1), (149999, 150000)])})
    return out
