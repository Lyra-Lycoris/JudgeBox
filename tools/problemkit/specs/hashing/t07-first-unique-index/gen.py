import random

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def cases():
    rng = random.Random(20261117)
    out = [
        {"id": "01", "input": "8\nabacabad\n"},
        {"id": "02", "input": "1\nz\n"},
        {"id": "03", "input": "6\naaaaaa\n"},
        {"id": "04", "input": "6\nabcdef\n"},
        {"id": "05", "input": "8\naabbccdd\n"},
        {"id": "06", "input": "2\nab\n"},
        {"id": "07", "input": "2\naa\n"},
    ]

    # 中等规模：字母表只有 3 个符号
    n = 1000
    s = "".join(rng.choice("abc") for _ in range(n))
    out.append({"id": "08", "input": "%d\n%s\n" % (n, s)})

    # 大数据：26 个字母均匀随机，几乎一定没有只出现一次的字符
    n = 1000000
    s = "".join(rng.choice(ALPHABET) for _ in range(n))
    out.append({"id": "09", "input": "%d\n%s\n" % (n, s)})

    # 大数据：首字符只出现一次
    n = 1000000
    body = "".join(rng.choice("abcdefghijklmnopqrstuvwxy") for _ in range(n - 1))
    out.append({"id": "10", "input": "%d\n%s\n" % (n, "z" + body)})

    # 大数据：前 25 个字母循环出现，只有一个 z 藏在中点
    n = 1000000
    base = "abcdefghijklmnopqrstuvwxy"
    chars = list((base * (n // len(base) + 1))[:n])
    chars[n // 2 - 1] = "z"
    out.append({"id": "11", "input": "%d\n%s\n" % (n, "".join(chars))})
    return out
