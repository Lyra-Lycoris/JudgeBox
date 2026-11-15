import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261116)
    out = [
        {"id": "01", "input": "7\n2 2 1 1 1 2 2\n"},
        {"id": "02", "input": "1\n42\n"},
        {"id": "03", "input": "5\n-7 -7 -7 -7 -7\n"},
        {"id": "04", "input": "9\n5 5 5 5 5 1 2 3 4\n"},
        {"id": "05", "input": "3\n4 9 4\n"},
        {"id": "06", "input": "2\n1000000000 1000000000\n"},
    ]

    # 中等规模：随机序列，再把前 600 个位置改成众数
    n = 1000
    a = [rng.randint(-1000, 1000) for _ in range(n)]
    a[:600] = [17] * 600
    rng.shuffle(a)
    out.append({"id": "07", "input": "%d\n%s\n" % (n, _line(a))})

    # 中等规模：众数刚好过半一点点
    n = 1001
    a = [rng.randint(10 ** 8, 10 ** 9) for _ in range(n)]
    a[:501] = [-3] * 501
    rng.shuffle(a)
    out.append({"id": "08", "input": "%d\n%s\n" % (n, _line(a))})

    # 大数据：全部相同
    n = 200000
    a = [10 ** 9] * n
    out.append({"id": "09", "input": "%d\n%s\n" % (n, _line(a))})

    # 大数据：众数 100001 个，其余随机
    n = 200000
    a = [rng.randint(0, 10 ** 9) for _ in range(n)]
    a[:100001] = [123456789] * 100001
    rng.shuffle(a)
    out.append({"id": "10", "input": "%d\n%s\n" % (n, _line(a))})
    return out
