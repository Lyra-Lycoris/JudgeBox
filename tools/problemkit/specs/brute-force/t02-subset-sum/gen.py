import random


def _line(values):
    return " ".join(str(v) for v in values)


def cases():
    rng = random.Random(20261114)
    out = []

    # 01 样例：1+2+3 = 2+4 = 6
    out.append({"id": "01", "input": "6 4\n1 2 3 4\n"})

    # 02 边界 n = 1，恰好命中
    out.append({"id": "02", "input": "7 1\n7\n"})

    # 03 边界 n = 1，无法命中
    out.append({"id": "03", "input": "8 1\n7\n"})

    # 04 全部相同：5+5+5 = 15
    out.append({"id": "04", "input": "15 6\n5 5 5 5 5 5\n"})

    # 05 含负数与 0：(-1) + (-2) = -3
    out.append({"id": "05", "input": "-3 5\n4 -1 -2 0 7\n"})

    # 06 目标为 0，空集即可达
    out.append({"id": "06", "input": "0 3\n5 6 -7\n"})

    # 07 18 个偶数，奇数目标必定不可达
    even = [rng.randrange(-500000000, 500000001) * 2 for _ in range(18)]
    out.append({"id": "07", "input": "%d %d\n%s\n" % (999999999, len(even), _line(even))})

    # 08 20 个大数，目标由随机子集求和得到
    big = [rng.randint(1, 10 ** 9) for _ in range(20)]
    picked = [v for v in big if rng.random() < 0.5] or [big[0]]
    out.append({"id": "08", "input": "%d %d\n%s\n" % (sum(picked), len(big), _line(big))})

    # 09 最坏情况：20 个互不相同的大随机数，需要枚举全部 2^20 个子集
    worst = rng.sample(range(1, 10 ** 9), 20)
    out.append({"id": "09", "input": "%d %d\n%s\n" % (sum(worst) - 1, len(worst), _line(worst))})

    # 10 20 个 1，目标 13
    ones = [1] * 20
    out.append({"id": "10", "input": "13 20\n%s\n" % _line(ones)})

    # 11 中等规模随机数据
    mid = [rng.randint(-1000, 1000) for _ in range(15)]
    picked = [v for v in mid if rng.random() < 0.5] or [mid[0]]
    out.append({"id": "11", "input": "%d %d\n%s\n" % (sum(picked), len(mid), _line(mid))})

    return out
