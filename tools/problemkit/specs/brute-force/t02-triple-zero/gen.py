import random


def _line(values):
    return " ".join(str(v) for v in values)


def cases():
    rng = random.Random(20261115)
    out = []

    # 01 样例：只有 (-1, 0, 1)
    out.append({"id": "01", "input": "3\n-1 0 1\n"})

    # 02 边界 n = 1
    out.append({"id": "02", "input": "1\n5\n"})

    # 03 边界 n = 2
    out.append({"id": "03", "input": "2\n-3 3\n"})

    # 04 全为 0：C(300, 3) = 4455100
    out.append({"id": "04", "input": "300\n%s\n" % _line([0] * 300)})

    # 05 全部相同（正数），答案为 0
    out.append({"id": "05", "input": "300\n%s\n" % _line([7] * 300)})

    # 06 全为 -1000000000：三项之和为负，答案为 0
    out.append({"id": "06", "input": "300\n%s\n" % _line([-1000000000] * 300)})

    # 07 小范围随机，重复多、三元组多
    small = [rng.randint(-5, 5) for _ in range(300)]
    out.append({"id": "07", "input": "300\n%s\n" % _line(small)})

    # 08 大范围随机，三元组稀少
    big = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(300)]
    out.append({"id": "08", "input": "300\n%s\n" % _line(big)})

    # 09 构造：100 个 x、100 个 -x、100 个 0，三元组数量很大
    x = 123456789
    mixed = [x] * 100 + [-x] * 100 + [0] * 100
    rng.shuffle(mixed)
    out.append({"id": "09", "input": "300\n%s\n" % _line(mixed)})

    # 10 奇数长度 n = 299 的随机数据
    odd = [rng.randint(-10, 10) for _ in range(299)]
    out.append({"id": "10", "input": "299\n%s\n" % _line(odd)})

    return out
