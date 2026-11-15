import random


def _join(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261115)
    out = []

    # 01 样例：1,2,5 凑 5 有 4 种
    out.append({"id": "01", "input": "3 5\n1 2 5\n"})

    # 02 无法凑出
    out.append({"id": "02", "input": "1 5\n3\n"})

    # 03 只有面额 1
    out.append({"id": "03", "input": "1 10\n1\n"})

    # 04 大数据：随机互不相同面额
    n, target = 100, 5000
    coins = sorted(rng.sample(range(1, 5001), n))
    out.append({"id": "04", "input": "%d %d\n%s\n" % (n, target, _join(coins))})

    # 05 面额恰好等于 target
    out.append({"id": "05", "input": "1 5000\n5000\n"})

    # 06 面额 1..100，target 5000，方案数很大需要取模
    coins = list(range(1, 101))
    out.append({"id": "06", "input": "%d 5000\n%s\n" % (len(coins), _join(coins))})

    # 07 target = 1
    out.append({"id": "07", "input": "2 1\n1 2\n"})

    # 08 随机中等
    n, target = 30, 300
    coins = sorted(rng.sample(range(1, 301), n))
    out.append({"id": "08", "input": "%d %d\n%s\n" % (n, target, _join(coins))})

    # 09 面额全为偶数，target 为奇数 => 0
    coins = [2 * i for i in range(1, 21)]
    out.append({"id": "09", "input": "%d 501\n%s\n" % (len(coins), _join(coins))})

    # 10 两种面额，答案 2501
    out.append({"id": "10", "input": "2 5000\n1 2\n"})

    # 11 面额互不相同且都大于 target
    out.append({"id": "11", "input": "3 4\n5 6 7\n"})

    return out
