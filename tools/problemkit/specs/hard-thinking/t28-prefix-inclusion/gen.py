import random


def _input(n, conds):
    parts = ["%d %d\n" % (n, len(conds))]
    for t, x in conds:
        parts.append("%d %d\n" % (t, x))
    return "".join(parts)


def _distinct(conds):
    seen = []
    for c in conds:
        if c not in seen:
            seen.append(c)
    return seen


def cases():
    rng = random.Random(20261121)
    out = []

    def add(n, conds):
        out.append({"id": "%02d" % (len(out) + 1), "input": _input(n, _distinct(conds))})

    # 01 样例：10 以内，偶数或第 1 位为 1
    add(10, [(1, 2), (2, 1)])

    # 02 边界：n = 1，含一个 k = 1 的条件（覆盖所有整数）
    add(1, [(1, 1), (2, 59)])

    # 03 边界：n = 1，只有「第 0 位为 1」成立
    add(1, [(2, 59), (2, 0), (1, 4)])

    # 04 边界：n = 2^59，最高的两位正好卡在边界上
    add(1 << 59, [(2, 59), (2, 58)])

    # 05 极值：n = 10^18，8 个低位条件
    add(10 ** 18, [(2, b) for b in range(8)])

    # 06 极值：n = 10^18，8 个整除条件（k = 2 .. 256）
    add(10 ** 18, [(1, 1 << p) for p in range(1, 9)])

    # 07 极值：n = 10^18，整除条件与低位条件互相冲突
    add(10 ** 18, [(1, 8), (1, 32), (1, 128), (1, 512), (2, 0), (2, 1), (2, 2), (2, 59)])

    # 08 极值：n = 10^18，8 个高位条件
    add(10 ** 18, [(2, b) for b in range(52, 60)])

    # 09 随机小数据：n <= 10^6，m = 6
    n = rng.randint(1, 10 ** 6)
    conds = []
    for _ in range(6):
        if rng.random() < 0.5:
            conds.append((1, 1 << rng.randint(0, 20)))
        else:
            conds.append((2, rng.randint(0, 59)))
    add(n, conds)

    # 10 随机大数据：n 接近 10^18，m = 8 混合条件
    n = rng.randint(10 ** 17, 10 ** 18)
    conds = []
    for _ in range(8):
        if rng.random() < 0.4:
            conds.append((1, 1 << rng.randint(1, 20)))
        else:
            conds.append((2, rng.randint(0, 59)))
    add(n, conds)

    # 11 极值：n = 10^18，一个 k = 1 的条件让答案恰为 n
    add(10 ** 18, [(1, 1), (1, 4), (1, 64), (2, 0), (2, 7), (2, 33), (2, 58), (2, 59)])

    # 12 随机中等数据：n 约 10^9，8 个条件且互不相同
    n = rng.randint(10 ** 8, 10 ** 9)
    conds = []
    for _ in range(8):
        if rng.random() < 0.5:
            conds.append((1, 1 << rng.randint(0, 20)))
        else:
            conds.append((2, rng.randint(0, 59)))
    add(n, conds)

    return out
