import random


def _line(values):
    return " ".join(str(x) for x in values)


def _shuffled_run(rng, start, length):
    values = list(range(start, start + length))
    rng.shuffle(values)
    return values


def cases():
    rng = random.Random(20261119)
    out = [
        {"id": "01", "input": "6\n100 4 200 1 3 2\n"},
        {"id": "02", "input": "1\n7\n"},
        {"id": "03", "input": "6\n5 5 5 5 5 5\n"},
        {"id": "04", "input": "7\n-3 -2 -1 0 1 2 3\n"},
        {"id": "05", "input": "8\n1 2 3 10 11 12 13 13\n"},
        {"id": "06", "input": "3\n-1000000000 1000000000 0\n"},
    ]

    # 中等规模：取值集中在一个小范围，重复很多
    n = 1000
    a = [rng.randint(-20, 20) for _ in range(n)]
    out.append({"id": "07", "input": "%d\n%s\n" % (n, _line(a))})

    # 中等规模：由 5 段长度为 200 的连续整数打乱而成
    parts = []
    for k in range(5):
        parts += _shuffled_run(rng, k * 100000, 200)
    rng.shuffle(parts)
    out.append({"id": "08", "input": "%d\n%s\n" % (len(parts), _line(parts))})

    # 大数据：1 到 200000 全部连续，打乱顺序
    a = _shuffled_run(rng, 1, 200000)
    out.append({"id": "09", "input": "%d\n%s\n" % (len(a), _line(a))})

    # 大数据：全部随机，最长连续段通常很短
    a = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(200000)]
    out.append({"id": "10", "input": "%d\n%s\n" % (len(a), _line(a))})

    # 大数据：贴着上界的一整段连续整数
    a = _shuffled_run(rng, 10 ** 9 - 199999, 200000)
    out.append({"id": "11", "input": "%d\n%s\n" % (len(a), _line(a))})
    return out
