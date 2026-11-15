import random


def _grid(rows):
    return "".join(" ".join(str(v) for v in row) + "\n" for row in rows)


def _query_lines(queries):
    return "".join("%d %d %d %d\n" % (x1, y1, x2, y2) for x1, y1, x2, y2 in queries)


def _random_queries(rng, q, n, m):
    queries = []
    for _ in range(q):
        x1 = rng.randint(1, n)
        x2 = rng.randint(x1, n)
        y1 = rng.randint(1, m)
        y2 = rng.randint(y1, m)
        queries.append((x1, y1, x2, y2))
    return queries


def cases():
    rng = random.Random(20261116)
    out = []

    # 01 样例
    out.append({"id": "01", "input": "3 4\n" + _grid([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
                + "2\n" + _query_lines([(1, 1, 3, 4), (2, 2, 3, 3)])})

    # 02 边界：1 x 1，负值
    out.append({"id": "02", "input": "1 1\n-1000000000\n1\n1 1 1 1\n"})

    # 03 边界：只有一行，全为 1e9
    out.append({"id": "03", "input": "1 500\n" + _grid([[1000000000] * 500]) + "1\n1 1 1 500\n"})

    # 04 边界：只有一列，正负交替
    col = [[1000000000 if i % 2 == 0 else -1000000000] for i in range(500)]
    out.append({"id": "04", "input": "500 1\n" + _grid(col) + "1\n1 1 500 1\n"})

    # 05 边界：500 x 500 全 0
    out.append({"id": "05", "input": "500 500\n" + _grid([[0] * 500 for _ in range(500)]) + "1\n1 1 500 500\n"})

    # 06 大数据：500 x 500 全 1e9，答案为 2.5e14
    out.append({"id": "06", "input": "500 500\n" + _grid([[1000000000] * 500 for _ in range(500)])
                + "1\n1 1 500 500\n"})

    # 07 大数据：500 x 500 全 -1e9
    out.append({"id": "07", "input": "500 500\n" + _grid([[-1000000000] * 500 for _ in range(500)])
                + "1\n1 1 500 500\n"})

    # 08 大数据：500 x 500 小范围随机 + 100000 次随机查询
    small = [[rng.randint(-1000, 1000) for _ in range(500)] for _ in range(500)]
    out.append({"id": "08", "input": "500 500\n" + _grid(small) + "100000\n"
                + _query_lines(_random_queries(rng, 100000, 500, 500))})

    # 09 大数据：200 x 300 全范围随机 + 100000 次随机查询
    wide = [[rng.randint(-10 ** 9, 10 ** 9) for _ in range(300)] for _ in range(200)]
    out.append({"id": "09", "input": "200 300\n" + _grid(wide) + "100000\n"
                + _query_lines(_random_queries(rng, 100000, 200, 300))})

    # 10 大数据：500 x 500 棋盘 ±1，查询全部为 3 x 3 小块
    board = [[1 if (i + j) % 2 == 0 else -1 for j in range(500)] for i in range(500)]
    queries = [(i, j, i + 2, j + 2) for i in range(1, 499, 10) for j in range(1, 499, 10)]
    out.append({"id": "10", "input": "500 500\n" + _grid(board) + "%d\n" % len(queries) + _query_lines(queries)})

    # 11 中等规模：40 x 40 随机 + 200 次随机查询
    medium = [[rng.randint(-10 ** 9, 10 ** 9) for _ in range(40)] for _ in range(40)]
    out.append({"id": "11", "input": "40 40\n" + _grid(medium) + "200\n"
                + _query_lines(_random_queries(rng, 200, 40, 40))})
    return out
