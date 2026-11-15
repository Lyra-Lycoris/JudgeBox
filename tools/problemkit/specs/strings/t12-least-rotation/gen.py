import random

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def cases():
    rng = random.Random(20261208)
    out = [
        {"id": "01", "input": "4\nbaca\n"},
        {"id": "02", "input": "1\na\n"},
        {"id": "03", "input": "5\naaaaa\n"},
        {"id": "04", "input": "3\ncba\n"},
        {"id": "05", "input": "6\nbanana\n"},
        {"id": "06", "input": "2\nba\n"},
        {"id": "07", "input": "7\nabababa\n"},
    ]

    # 中等规模：三字母随机串
    n = 1000
    s = "".join(rng.choice("abc") for _ in range(n))
    out.append({"id": "08", "input": "%d\n%s\n" % (n, s)})

    # 大数据：26 字母随机串
    n = 200000
    s = "".join(rng.choice(LETTERS) for _ in range(n))
    out.append({"id": "09", "input": "%d\n%s\n" % (n, s)})

    # 大数据：交替串，多个循环移位并列最小，答案是 0
    n = 200000
    out.append({"id": "10", "input": "%d\n%s\n" % (n, "ab" * (n // 2))})

    # 大数据：几乎全是 a，末尾一个 b
    n = 200000
    out.append({"id": "11", "input": "%d\n%s\n" % (n, "a" * (n - 1) + "b")})

    # 大数据：以 b 开头、以 a 结尾，最小循环移位在最后
    n = 200000
    out.append({"id": "12", "input": "%d\n%s\n" % (n, "b" * (n - 1) + "a")})
    return out
