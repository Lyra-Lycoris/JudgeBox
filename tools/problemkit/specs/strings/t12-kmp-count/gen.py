import random


def cases():
    rng = random.Random(20261202)
    out = [
        {"id": "01", "input": "9\nababababa\n3\naba\n"},
        {"id": "02", "input": "1\na\n1\na\n"},
        {"id": "03", "input": "1\na\n1\nb\n"},
        {"id": "04", "input": "5\naaaaa\n2\naa\n"},
        {"id": "05", "input": "6\nabcabc\n6\nabcabc\n"},
        {"id": "06", "input": "7\nabcdefg\n3\nxyz\n"},
        {"id": "07", "input": "3\naba\n2\nab\n"},
    ]

    # 中等规模：二元字母表随机串
    n = 2000
    s = "".join(rng.choice("ab") for _ in range(n))
    m = 6
    p = "".join(rng.choice("ab") for _ in range(m))
    out.append({"id": "08", "input": "%d\n%s\n%d\n%s\n" % (n, s, m, p)})

    # 大数据：几乎全是 a，模式串很长，只有最后一次匹配
    n = 200000
    s = "a" * (n - 1) + "b"
    m = 1000
    p = "a" * (m - 1) + "b"
    out.append({"id": "09", "input": "%d\n%s\n%d\n%s\n" % (n, s, m, p)})

    # 大数据：全是 a，模式串 aa...a，重叠匹配极多
    n = 200000
    s = "a" * n
    m = 1000
    p = "a" * m
    out.append({"id": "10", "input": "%d\n%s\n%d\n%s\n" % (n, s, m, p)})

    # 大数据：交替串，模式串是偶数长度的 "ab" 重复
    n = 200000
    s = "ab" * (n // 2)
    m = 100
    p = "ab" * (m // 2)
    out.append({"id": "11", "input": "%d\n%s\n%d\n%s\n" % (n, s, m, p)})

    # 大数据：26 个字母的随机串，模式串取自串中间，至少命中一次
    n = 200000
    s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))
    m = 7
    p = s[100000:100000 + m]
    out.append({"id": "12", "input": "%d\n%s\n%d\n%s\n" % (n, s, m, p)})
    return out
