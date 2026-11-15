import random


def line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261121)
    out = []

    def add(n, m, r, c):
        assert len(r) == n and len(c) == m and sum(r) == sum(c), (n, m, r, c)
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d %d\n%s\n%s\n" % (n, m, line(r), line(c))})

    def add_from_grid(g):
        n, m = len(g), len(g[0])
        r = [sum(row) for row in g]
        c = [sum(g[i][j] for i in range(n)) for j in range(m)]
        add(n, m, r, c)

    add(2, 3, [3, 3], [2, 2, 2])
    add(1, 1, [0], [0])
    add(1, 1, [1000000000], [1000000000])
    add(1, 5, [7], [1, 2, 3, 0, 1])
    add(5, 1, [1, 2, 3, 0, 1], [7])
    add(2, 2, [1000000000, 0], [0, 1000000000])
    add(3, 4, [6, 0, 9], [1, 5, 4, 5])

    add_from_grid([[rng.randint(0, 1000) for _ in range(30)] for _ in range(20)])
    add_from_grid([[rng.randint(0, 10000000) for _ in range(100)] for _ in range(100)])
    add(100, 100, [0] * 100, [0] * 100)

    row = [0] * 100
    col = [0] * 100
    row[0] = 1000000000
    col[99] = 1000000000
    add(100, 100, row, col)

    add(100, 1, [10000000] * 100, [1000000000])
    return out
