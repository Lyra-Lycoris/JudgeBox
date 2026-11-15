import random


def pack(grid):
    lines = ["%d %d" % (len(grid), len(grid[0]))]
    for row in grid:
        lines.append(" ".join(str(x) for x in row))
    return "\n".join(lines) + "\n"


def random_grid(rng, n, m, p):
    grid = [[1 if rng.random() < p else 0 for _ in range(m)] for _ in range(n)]
    grid[0][0] = 0
    grid[n - 1][m - 1] = 0
    return grid


def cases():
    rng = random.Random(20261117)
    out = [{"id": "01", "input": pack([[0, 0, 0], [0, 1, 0], [0, 0, 0]])}]
    out.append({"id": "02", "input": pack([[0]])})
    out.append({"id": "03", "input": pack([[1]])})
    out.append({"id": "04", "input": pack([[0, 0, 0, 0, 0]])})
    out.append({"id": "05", "input": pack([[0], [0], [0], [0], [0]])})
    out.append({"id": "06", "input": pack([[0, 1], [1, 0]])})
    out.append({"id": "07", "input": pack([[0, 0], [0, 0]])})
    out.append({"id": "08", "input": pack(random_grid(rng, 5, 5, 0.25))})
    out.append({"id": "09", "input": pack([[0] * 500 for _ in range(500)])})
    out.append({"id": "10", "input": pack(random_grid(rng, 500, 500, 0.1))})
    out.append({"id": "11", "input": pack(random_grid(rng, 500, 500, 0.5))})

    blocked = [[1] * 500 for _ in range(500)]
    blocked[0][0] = 0
    blocked[499][499] = 0
    out.append({"id": "12", "input": pack(blocked)})
    return out
