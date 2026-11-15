import random


def cases():
    rng = random.Random(20261203)
    out = [
        {"id": "01", "input": "9\nabcabcabc\n"},
        {"id": "02", "input": "1\na\n"},
        {"id": "03", "input": "4\naaaa\n"},
        {"id": "04", "input": "4\nabab\n"},
        {"id": "05", "input": "5\nabcab\n"},
        {"id": "06", "input": "6\naabaab\n"},
        {"id": "07", "input": "7\nabcabca\n"},
    ]

    # 中等规模：3 个字符一段，恰好能拼成整串
    n = 999
    out.append({"id": "08", "input": "%d\n%s\n" % (n, "abc" * (n // 3))})

    # 中等规模：26 字母随机，答案几乎一定是 n
    n = 1000
    s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))
    out.append({"id": "09", "input": "%d\n%s\n" % (n, s)})

    # 大数据：4 个字符一段
    n = 200000
    out.append({"id": "10", "input": "%d\n%s\n" % (n, "abcd" * (n // 4))})

    # 大数据：几乎全是 a，末尾一个 b，循环节只能是 n
    n = 200000
    out.append({"id": "11", "input": "%d\n%s\n" % (n, "a" * (n - 1) + "b")})

    # 大数据：两个字符一段
    n = 200000
    out.append({"id": "12", "input": "%d\n%s\n" % (n, "ab" * (n // 2))})
    return out
