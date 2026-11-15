import random


def _case(n, a):
    return "%d\n%s\n" % (n, " ".join(str(x) for x in a))


def cases():
    rng = random.Random(20261117)
    out = []

    def add(n, a):
        assert len(a) == n
        out.append({"id": "%02d" % (len(out) + 1), "input": _case(n, a)})

    # 01：样例
    add(2, [1, 1])
    # 02：只有一堆一颗，先手被迫取走最后一颗
    add(1, [1])
    # 03：只有一堆两颗
    add(1, [2])
    # 04：全为 1，偶数堆
    add(8, [1] * 8)
    # 05：全为 1，奇数堆
    add(9, [1] * 9)
    # 06：两堆相同的大堆，异或和为 0
    add(2, [5, 5])
    # 07：三堆，其中两堆接近上限
    add(3, [10 ** 9, 10 ** 9 - 1, 1])
    # 08：全为 1 之外还有大堆
    add(4, [1, 1, 1, 5])
    # 09：中等规模随机
    add(1000, [rng.randint(1, 10 ** 9) for _ in range(1000)])
    # 10：中等规模，成对出现（异或和为 0）
    add(2000, [v for _ in range(1000) for v in (rng.randint(1, 10 ** 9),) * 2])
    # 11：大数据，全为 1，偶数堆
    add(200000, [1] * 200000)
    # 12：大数据，全为 1，奇数堆
    add(199999, [1] * 199999)
    # 13：大数据随机
    add(200000, [rng.randint(1, 10 ** 9) for _ in range(200000)])
    return out
