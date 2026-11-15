import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261115)
    out = [
        {"id": "01", "input": "7\n1 2 2 3 3 3 4\n"},
        {"id": "02", "input": "1\n5\n"},
        {"id": "03", "input": "5\n9 9 9 9 9\n"},
        {"id": "04", "input": "6\n-1 -2 -2 -3 -3 -3\n"},
        {"id": "05", "input": "2\n1000000000 -1000000000\n"},
    ]

    # 中等规模：取值范围很小，很多数并列
    n = 1000
    a = [rng.randint(-5, 5) for _ in range(n)]
    out.append({"id": "06", "input": "%d\n%s\n" % (n, _line(a))})

    # 中等规模：构造一个出现 500 次的数
    n = 1000
    a = [rng.randint(0, 10 ** 9) for _ in range(n)]
    a[:500] = [7] * 500
    rng.shuffle(a)
    out.append({"id": "07", "input": "%d\n%s\n" % (n, _line(a))})

    # 大数据：全部相同
    n = 200000
    a = [-10 ** 9] * n
    out.append({"id": "08", "input": "%d\n%s\n" % (n, _line(a))})

    # 大数据：取值范围很小，众数次数很大
    n = 200000
    a = [rng.randint(0, 999) for _ in range(n)]
    out.append({"id": "09", "input": "%d\n%s\n" % (n, _line(a))})

    # 大数据：取值全异，答案为 1
    n = 200000
    a = list(range(1, n + 1))
    rng.shuffle(a)
    out.append({"id": "10", "input": "%d\n%s\n" % (n, _line(a))})
    return out
