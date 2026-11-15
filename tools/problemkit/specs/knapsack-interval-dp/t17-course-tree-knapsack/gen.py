import random


def _join(values):
    return " ".join(str(x) for x in values)


def _pack(n, k, parent, profit):
    return "%d %d\n%s\n%s\n" % (n, k, _join(parent), _join(profit))


def _forest(n, rng, lo=-10 ** 9, hi=10 ** 9):
    order = list(range(1, n + 1))
    rng.shuffle(order)
    par = [0] * (n + 1)
    for idx in range(1, n):
        node = order[idx]
        candidates = [0] + order[:idx]
        par[node] = rng.choice(candidates)
    profit = [rng.randint(lo, hi) for _ in range(n)]
    return par[1:], profit


def _chain(n, rng, lo=-10 ** 9, hi=10 ** 9):
    par = [0] + [i - 1 for i in range(2, n + 1)]
    profit = [rng.randint(lo, hi) for _ in range(n)]
    return par, profit


def _star(n, rng, lo=-10 ** 9, hi=10 ** 9):
    par = [0] * n
    profit = [rng.randint(lo, hi) for _ in range(n)]
    return par, profit


def cases():
    rng = random.Random(20261121)
    out = []

    # 01 样例
    out.append({"id": "01", "input": _pack(4, 2, [0, 1, 1, 2], [3, 2, 5, 4])})

    # 02 只有一门课
    out.append({"id": "02", "input": _pack(1, 1, [0], [5])})

    # 03 收益为负数
    out.append({"id": "03", "input": _pack(1, 1, [0], [-5])})

    # 04 一条长度为 200 的链，只能取前缀
    par, profit = _chain(200, rng, 0, 10 ** 9)
    out.append({"id": "04", "input": _pack(200, 100, par, profit)})

    # 05 所有收益都是负数
    par, profit = _forest(50, rng, -10 ** 9, -1)
    out.append({"id": "05", "input": _pack(50, 10, par, profit)})

    # 06 菊花图：所有课都没有先修要求，取收益最大的 100 门
    par, profit = _star(200, rng, 0, 10 ** 9)
    out.append({"id": "06", "input": _pack(200, 100, par, profit)})

    # 07 随机森林
    par, profit = _forest(200, rng)
    out.append({"id": "07", "input": _pack(200, 50, par, profit)})

    # 08 随机森林，取全部课程
    par, profit = _forest(200, rng)
    out.append({"id": "08", "input": _pack(200, 200, par, profit)})

    # 09 只取一门课
    par, profit = _star(200, rng, -10 ** 9, 10 ** 9)
    out.append({"id": "09", "input": _pack(200, 1, par, profit)})

    # 10 链上的全部课程
    par, profit = _chain(200, rng)
    out.append({"id": "10", "input": _pack(200, 200, par, profit)})

    # 11 随机中等
    par, profit = _forest(100, rng, -1000, 1000)
    out.append({"id": "11", "input": _pack(100, 5, par, profit)})

    return out
