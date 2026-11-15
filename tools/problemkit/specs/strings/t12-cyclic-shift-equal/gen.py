import random

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def cases():
    rng = random.Random(20261201)
    out = [
        {"id": "01", "input": "5\nabcde\ncdeab\n"},
        {"id": "02", "input": "1\na\na\n"},
        {"id": "03", "input": "1\na\nb\n"},
        {"id": "04", "input": "5\nabcde\nabced\n"},
        {"id": "05", "input": "2\nab\nba\n"},
        {"id": "06", "input": "3\naaa\naaa\n"},
    ]

    # 中等规模：随机串，取一个真实的循环移位
    n = 1000
    s = "".join(rng.choice(LETTERS) for _ in range(n))
    k = rng.randrange(n)
    out.append({"id": "07", "input": "%d\n%s\n%s\n" % (n, s, s[k:] + s[:k])})

    # 中等规模：字母表只有两个符号，扰动一个字符
    n = 1000
    s = "".join(rng.choice("ab") for _ in range(n))
    k = rng.randrange(n)
    t = list(s[k:] + s[:k])
    t[n // 2] = "b" if t[n // 2] == "a" else "a"
    out.append({"id": "08", "input": "%d\n%s\n%s\n" % (n, s, "".join(t))})

    # 大数据：n = 200000 的真实循环移位
    n = 200000
    big = "".join(rng.choice(LETTERS) for _ in range(n))
    k = 12345
    out.append({"id": "09", "input": "%d\n%s\n%s\n" % (n, big, big[k:] + big[:k])})

    # 大数据：全是同一个字符
    n = 200000
    same = "a" * n
    out.append({"id": "10", "input": "%d\n%s\n%s\n" % (n, same, same)})

    # 大数据：只差一个字符（不再是循环移位）
    n = 200000
    other = list(same)
    other[n // 3] = "b"
    out.append({"id": "11", "input": "%d\n%s\n%s\n" % (n, same, "".join(other))})

    # 大数据：字符集合相同但顺序不同（交换两个相邻且不同的字符）
    n = 200000
    s2 = "".join(rng.choice(LETTERS) for _ in range(n))
    t2 = list(s2)
    i = n // 3
    while i + 1 < n and s2[i] == s2[i + 1]:
        i += 1
    t2[i], t2[i + 1] = t2[i + 1], t2[i]
    out.append({"id": "12", "input": "%d\n%s\n%s\n" % (n, s2, "".join(t2))})
    return out
