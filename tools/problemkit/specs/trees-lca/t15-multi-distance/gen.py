import random


def pack_group(n, edges, queries):
    parts = ["%d" % n]
    parts += ["%d %d" % (u, v) for u, v in edges]
    parts.append("%d" % len(queries))
    parts += ["%d %d" % (a, b) for a, b in queries]
    return parts


def pack(groups):
    parts = ["%d" % len(groups)]
    for n, edges, queries in groups:
        parts += pack_group(n, edges, queries)
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
    rng = random.Random(20261121)
    out = []
    out.append({"id": "01", "input": pack([
        (3, [(1, 2), (2, 3)], [(1, 3), (2, 2)]),
        (1, [], [(1, 1)]),
    ])})
    out.append({"id": "02", "input": pack([(1, [], [(1, 1), (1, 1)])])})
    out.append({"id": "03", "input": pack([
        (10, path_edges(10), [(1, 10), (10, 10), (5, 7), (2, 3)]),
    ])})
    out.append({"id": "04", "input": pack([
        (8, star_edges(8), [(2, 3), (4, 8), (1, 5)]),
        (6, path_edges(6), [(1, 6), (3, 4), (2, 2)]),
        (9, random_tree(rng, 9), [(1, 9), (4, 7), (5, 5)]),
    ])})
    out.append({"id": "05", "input": pack([
        (20, random_tree(rng, 20), random_pairs(rng, 10, 20)) for _ in range(5)
    ])})
    out.append({"id": "06", "input": pack([
        (5000, random_tree(rng, 5000), random_pairs(rng, 5000, 5000)),
    ])})
    out.append({"id": "07", "input": pack([
        (150000, path_edges(150000), random_pairs(rng, 150000, 150000)),
    ])})
    out.append({"id": "08", "input": pack([
        (70000, random_tree(rng, 70000), random_pairs(rng, 70000, 70000)),
        (70000, random_tree(rng, 70000), random_pairs(rng, 70000, 70000)),
    ])})
    out.append({"id": "09", "input": pack([
        (30000, random_tree(rng, 30000), random_pairs(rng, 30000, 30000)) for _ in range(5)
    ])})
    out.append({"id": "10", "input": pack([
        (150000, star_edges(150000), random_pairs(rng, 150000, 150000)),
    ])})
    return out
