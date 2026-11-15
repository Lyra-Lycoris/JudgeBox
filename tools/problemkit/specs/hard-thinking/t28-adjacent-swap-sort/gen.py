import random


def _case(n, a):
    return "%d\n%s\n" % (n, " ".join(str(x) for x in a))


def cases():
    rng = random.Random(20261116)
    out = []

    def add(n, a):
        assert len(a) == n
        out.append({"id": "%02d" % (len(out) + 1), "input": _case(n, a)})

    # 01：样例
    add(5, [2, 4, 1, 3, 3])
    # 02：单个元素
    add(1, [0])
    # 03：已经有序
    add(6, [1, 2, 3, 4, 5, 6])
    # 04：完全逆序
    add(6, [6, 5, 4, 3, 2, 1])
    # 05：全部相同
    add(8, [4] * 8)
    # 06：值域很小的随机（大量重复）
    add(20, [rng.randint(1, 3) for _ in range(20)])
    # 07：负数与重复
    add(30, [rng.randint(-5, 5) for _ in range(30)])
    # 08：中等规模随机
    add(1000, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(1000)])
    # 09：大数据，已排序
    add(200000, list(range(200000)))
    # 10：大数据，完全逆序
    add(200000, list(range(200000, 0, -1)))
    # 11：大数据随机
    add(200000, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(200000)])
    # 12：大数据，值域很小
    add(200000, [rng.randint(0, 1) for _ in range(200000)])
    return out
