import random


def _fmt(pairs):
    return "".join("%d %d\n" % (u, v) for u, v in pairs)


def cases():
    rng = random.Random(20261116)
    out = []

    # 01 样例：(1,3) 是亲戚，(1,4) 不是，(5,5) 是同一个人
    out.append({"id": "01", "input": "6 2\n" + _fmt([(1, 2), (2, 3)]) + "3\n" + _fmt([(1, 3), (1, 4), (5, 5)])})

    # 02 只有一个点，没有亲戚关系，询问自己
    out.append({"id": "02", "input": "1 0\n1\n" + _fmt([(1, 1)])})

    # 03 没有任何亲戚关系，所有询问都不是亲戚
    out.append({"id": "03", "input": "5 0\n3\n" + _fmt([(1, 2), (2, 3), (4, 5)])})

    # 04 一条链把 6 个人全连起来，所有询问都是亲戚
    out.append({"id": "04", "input": "6 5\n" + _fmt([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]) + "4\n"
                + _fmt([(1, 6), (2, 5), (3, 3), (4, 6)])})

    # 05 只有两个人：正向、反向、自己都算亲戚
    out.append({"id": "05", "input": "2 1\n" + _fmt([(1, 2)]) + "3\n" + _fmt([(1, 2), (2, 1), (1, 1)])})

    # 06 中等：1000 个人连成一条链，1000 个随机询问
    n = 1000
    rel = [(i, i + 1) for i in range(1, n)]
    qs = [(rng.randint(1, n), rng.randint(1, n)) for _ in range(1000)]
    out.append({"id": "06", "input": "%d %d\n" % (n, len(rel)) + _fmt(rel) + "%d\n" % len(qs) + _fmt(qs)})

    # 07 中等：5000 个人、5000 条随机关系、5000 个随机询问
    n, k = 5000, 5000
    rel = []
    for _ in range(k):
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        rel.append((u, v))
    qs = [(rng.randint(1, n), rng.randint(1, n)) for _ in range(5000)]
    out.append({"id": "07", "input": "%d %d\n" % (n, k) + _fmt(rel) + "%d\n" % len(qs) + _fmt(qs)})

    # 08 大数据：200000 个人连成一条链，60000 个询问
    n = 200000
    rel = [(i, i + 1) for i in range(1, n)]
    qs = [(1, rng.randint(1, n)) for _ in range(30000)]
    qs += [(rng.randint(1, n), n) for _ in range(30000)]
    out.append({"id": "08", "input": "%d %d\n" % (n, len(rel)) + _fmt(rel) + "%d\n" % len(qs) + _fmt(qs)})

    # 09 大数据：200000 个人、100000 条随机关系、100000 个随机询问
    n, k = 200000, 100000
    rel = []
    for _ in range(k):
        u = rng.randint(1, n)
        v = rng.randint(1, n - 1)
        if v >= u:
            v += 1
        rel.append((u, v))
    qs = []
    for _ in range(k):
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        qs.append((u, v))
    out.append({"id": "09", "input": "%d %d\n" % (n, k) + _fmt(rel) + "%d\n" % len(qs) + _fmt(qs)})

    # 10 大数据边界：200000 个人、没有任何关系，一半询问自己、一半询问别人
    n = 200000
    qs = [(i + 1, i + 1) for i in range(n // 2)]
    qs += [(i + 1, (i + 1) % n + 1) for i in range(n // 2)]
    out.append({"id": "10", "input": "%d 0\n" % n + "%d\n" % len(qs) + _fmt(qs)})

    return out
