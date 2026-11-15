import random


def pack(n, r, pairs):
    parts = ["%d %d" % (n, r)]
    parts += ["%d %d" % (l, rr) for l, rr in pairs]
    return "\n".join(parts) + "\n"


def left_chain(n):
    pairs = []
    for v in range(1, n + 1):
        pairs.append((v + 1 if v < n else 0, 0))
    return pairs


def complete(n):
    pairs = []
    for v in range(1, n + 1):
        l = 2 * v if 2 * v <= n else 0
        rr = 2 * v + 1 if 2 * v + 1 <= n else 0
        pairs.append((l, rr))
    return pairs


def random_binary(rng, n):
    left = [0] * (n + 1)
    right = [0] * (n + 1)
    slots = [(1, 0), (1, 1)]
    for v in range(2, n + 1):
        idx = rng.randrange(len(slots))
        u, side = slots[idx]
        slots[idx] = slots[-1]
        slots.pop()
        if side == 0:
            left[u] = v
        else:
            right[u] = v
        slots.append((v, 0))
        slots.append((v, 1))
    return [(left[v], right[v]) for v in range(1, n + 1)]


def cases():
    rng = random.Random(20261120)
    out = []
    out.append({"id": "01", "input": pack(7, 1, [(2, 3), (4, 5), (6, 7), (0, 0), (0, 0), (0, 0), (0, 0)])})
    out.append({"id": "02", "input": pack(1, 1, [(0, 0)])})
    out.append({"id": "03", "input": pack(3, 1, [(0, 2), (0, 3), (0, 0)])})
    out.append({"id": "04", "input": pack(6, 1, left_chain(6))})
    out.append({"id": "05", "input": pack(6, 4, [(0, 0), (1, 3), (0, 0), (2, 6), (0, 0), (5, 0)])})
    out.append({"id": "06", "input": pack(8, 1, complete(8))})
    out.append({"id": "07", "input": pack(100, 1, random_binary(rng, 100))})
    out.append({"id": "08", "input": pack(5000, 1, random_binary(rng, 5000))})
    out.append({"id": "09", "input": pack(200000, 1, left_chain(200000))})
    out.append({"id": "10", "input": pack(200000, 1, random_binary(rng, 200000))})
    out.append({"id": "11", "input": pack(200000, 1, complete(200000))})
    return out
