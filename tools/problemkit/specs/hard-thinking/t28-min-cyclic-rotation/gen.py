import random


def _line(values):
    return " ".join(str(x) for x in values)


def _case(n, a):
    return "%d\n%s\n" % (n, _line(a))


def cases():
    rng = random.Random(20261114)
    out = []

    def add(n, a):
        out.append({"id": "%02d" % (len(out) + 1), "input": _case(n, a)})

    # 01：样例
    add(6, [3, 1, 4, 1, 5, 9])
    # 02：只有一个元素
    add(1, [-5])
    # 03：两个元素，需要移位
    add(2, [2, 1])
    # 04：全部相同
    add(10, [7] * 10)
    # 05：严格递增，最小移位是原序列
    add(1000, list(range(1, 1001)))
    # 06：严格递减，最小移位是最后一个元素打头
    add(1000, list(range(1000, 0, -1)))
    # 07：两段重复的周期序列
    add(2000, [1, 2] * 1000)
    # 08：中等规模随机，值域很小（大量相同元素）
    add(5000, [rng.randint(0, 2) for _ in range(5000)])
    # 09：中等规模随机负数
    add(20000, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(20000)])
    # 10：大数据，全部相同（朴素比较会退化）
    add(200000, [42] * 200000)
    # 11：大数据，值域很小
    add(200000, [rng.randint(0, 3) for _ in range(200000)])
    # 12：大数据，随机大值
    add(200000, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(200000)])
    return out
