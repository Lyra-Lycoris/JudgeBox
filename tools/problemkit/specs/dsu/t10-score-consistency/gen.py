import random


def _fmt(rel):
    return "".join("%d %d %d\n" % (a, b, c) for a, b, c in rel)


def _values(rng, n, low, high):
    return [0] + [rng.randint(low, high) for _ in range(n)]


def _consistent(rng, n, k, val):
    rel = []
    for i in range(2, min(n, k) + 1):
        p = rng.randint(1, i - 1)
        rel.append((p, i, val[p] - val[i]))
    while len(rel) < k:
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        rel.append((u, v, val[u] - val[v]))
    return rel


def cases():
    rng = random.Random(20261120)
    out = []

    # 01 样例：前两条推出 x1 - x3 = 2，与第三条一致
    out.append({"id": "01", "input": "4 3\n" + _fmt([(1, 2, 3), (2, 3, -1), (1, 3, 2)])})

    # 02 没有学生以外的人，也没有陈述
    out.append({"id": "02", "input": "1 0\n"})

    # 03 自己比自己高 0 分
    out.append({"id": "03", "input": "1 1\n" + _fmt([(1, 1, 0)])})

    # 04 自己比自己高 5 分，矛盾
    out.append({"id": "04", "input": "1 1\n" + _fmt([(1, 1, 5)])})

    # 05 三条陈述绕成一圈，加起来不等于 0，矛盾
    out.append({"id": "05", "input": "3 3\n" + _fmt([(1, 2, 1), (2, 3, 1), (1, 3, 5)])})

    # 06 带负数的一条链，完全一致
    out.append({"id": "06", "input": "4 3\n" + _fmt([(1, 2, -3), (2, 3, 4), (3, 4, -5)])})

    # 07 随机中等：5000 个学生、8000 条陈述，由真实分数生成，一致
    n, k = 5000, 8000
    val = _values(rng, n, -1000, 1000)
    out.append({"id": "07", "input": "%d %d\n" % (n, k) + _fmt(_consistent(rng, n, k, val))})

    # 08 同样的规模，最后混进一条错误陈述，矛盾
    val = _values(rng, n, -1000, 1000)
    rel = _consistent(rng, n, k - 1, val)
    rel.append((1, 2, val[1] - val[2] + 1))
    out.append({"id": "08", "input": "%d %d\n" % (n, k) + _fmt(rel)})

    # 09 大数据：200000 个学生、120000 条陈述，一致
    n, k = 200000, 120000
    val = _values(rng, n, -1000, 1000)
    out.append({"id": "09", "input": "%d %d\n" % (n, k) + _fmt(_consistent(rng, n, k, val))})

    # 10 大数据：同样的输入再补一条错误陈述，矛盾
    val = _values(rng, n, -1000, 1000)
    rel = _consistent(rng, n, k - 1, val)
    rel.append((1, 2, val[1] - val[2] + 1))
    out.append({"id": "10", "input": "%d %d\n" % (n, k) + _fmt(rel)})

    # 11 大数据：所有陈述都是 a == b 且 c == 0，显然一致
    n, k = 200000, 100000
    rel = []
    for i in range(k):
        v = i % n + 1
        rel.append((v, v, 0))
    out.append({"id": "11", "input": "%d %d\n" % (n, k) + _fmt(rel)})

    # 12 较长的链，边权取到 ±10^9 的极值，路径上的差值会累积到 10^13 量级
    n = 30000
    rel = []
    for i in range(1, n):
        c = 10 ** 9 if i % 2 == 1 else -10 ** 9
        rel.append((i, i + 1, c))
    out.append({"id": "12", "input": "%d %d\n" % (n, len(rel)) + _fmt(rel)})

    return out
