import random


def pack(t, rows):
    lines = ["%d %d %d" % (len(rows), len(rows[0]), t)]
    for row in rows:
        lines.append(" ".join(str(x) for x in row))
    return "\n".join(lines) + "\n"


def sorted_rows(k, m, lo, hi, rng):
    return [sorted(rng.randint(lo, hi) for _ in range(m)) for _ in range(k)]


def cases():
    rng = random.Random(20260902)
    out = [{"id": "01", "input": pack(5, [[1, 4, 7], [2, 5, 8], [3, 6, 9]])}]
    out.append({"id": "02", "input": pack(1, [[-5]])})
    out.append({"id": "03", "input": pack(12, [[7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7]])})
    out.append({"id": "04", "input": pack(4, [[-9, -5, -1], [-8, -2, 0]])})
    out.append({"id": "05", "input": pack(1, [[-1000000000, 0], [5, 6], [1000000000, 1000000000]])})
    out.append({"id": "06", "input": pack(20, [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10],
                                              [11, 12, 13, 14, 15], [16, 17, 18, 19, 20]])})
    out.append({"id": "07", "input": pack(2000, sorted_rows(50, 60, -10 ** 6, 10 ** 6, rng))})
    out.append({"id": "08", "input": pack(80000, sorted_rows(400, 400, -10 ** 9, 10 ** 9, rng))})
    out.append({"id": "09", "input": pack(160000, sorted_rows(400, 400, 0, 0, rng))})
    return out
