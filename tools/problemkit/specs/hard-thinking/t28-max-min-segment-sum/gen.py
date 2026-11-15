import random


def _case(n, k, a):
    return "%d %d\n%s\n" % (n, k, " ".join(str(x) for x in a))


def cases():
    rng = random.Random(20261115)
    out = []

    def add(n, k, a):
        assert len(a) == n
        out.append({"id": "%02d" % (len(out) + 1), "input": _case(n, k, a)})

    # 01：样例
    add(5, 3, [1, 2, 3, 4, 5])
    # 02：只有一个元素
    add(1, 1, [7])
    # 03：只切一段，答案是总和
    add(6, 1, [4, 1, 5, 9, 2, 6])
    # 04：每段一个元素，答案是最小元素
    add(8, 8, [9, 3, 7, 1, 8, 2, 6, 5])
    # 05：全部相同
    add(10, 4, [5] * 10)
    # 06：中等规模随机
    add(1000, 7, [rng.randint(1, 100) for _ in range(1000)])
    # 07：大量 1，可以切得很碎
    add(5000, 2500, [1] * 5000)
    # 08：中等规模，k 接近 n
    add(2000, 1999, [rng.randint(1, 10 ** 9) for _ in range(2000)])
    # 09：大数据随机
    add(200000, 97, [rng.randint(1, 10 ** 9) for _ in range(200000)])
    # 10：大数据，k = 2
    add(200000, 2, [rng.randint(1, 10 ** 9) for _ in range(200000)])
    # 11：大数据，值全部是最大值
    add(200000, 33333, [10 ** 9] * 200000)
    # 12：大数据，只有首尾是大元素
    add(200000, 3, [10 ** 9] + [1] * 199998 + [10 ** 9])
    # 13：大数据，k = n（每段只剩一个元素，最坏情况）
    add(200000, 200000, [rng.randint(1, 10 ** 9) for _ in range(200000)])
    return out
