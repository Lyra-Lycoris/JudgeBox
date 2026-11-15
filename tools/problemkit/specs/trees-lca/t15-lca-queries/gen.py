import random


def pack(n, edges, queries):
    parts = ["%d" % n]
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
    rng = random.Random(20261115)
    out = []
    out.append({"id": "01", "input": pack(
        7, [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7)],
        [(4, 5), (5, 7), (6, 7), (4, 4)])})
    out.append({"id": "02", "input": pack(1, [], [(1, 1)])})
    out.append({"id": "03", "input": pack(
        10, path_edges(10), [(1, 10), (10, 10), (5, 7), (9, 10), (2, 3), (6, 4)])})
    out.append({"id": "04", "input": pack(8, star_edges(8), [(2, 3), (4, 8), (1, 5), (6, 7)])})
    out.append({"id": "05", "input": pack(100, random_tree(rng, 100), random_pairs(rng, 100, 100))})
    out.append({"id": "06", "input": pack(5000, random_tree(rng, 5000), random_pairs(rng, 5000, 5000))})
    out.append({"id": "07", "input": pack(150000, path_edges(150000), random_pairs(rng, 150000, 150000))})
    out.append({"id": "08", "input": pack(150000, random_tree(rng, 150000), random_pairs(rng, 150000, 150000))})
    out.append({"id": "09", "input": pack(150000, star_edges(150000), random_pairs(rng, 150000, 150000))})
    return out
