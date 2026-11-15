import random

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def cases():
    rng = random.Random(20261118)
    out = [
        {"id": "01", "input": "6\nlisten silent enlist inlets google gogole\n"},
        {"id": "02", "input": "1\na\n"},
        {"id": "03", "input": "4\nabc abc abc abc\n"},
        {"id": "04", "input": "4\nab ac ad ae\n"},
        {"id": "05", "input": "4\nabc bca cab abc\n"},
        {"id": "06", "input": "2\nab ba\n"},
    ]

    # 中等规模：长度为 3 的随机单词，大量碰撞
    n = 1000
    words = ["".join(rng.choice("abcd") for _ in range(3)) for _ in range(n)]
    out.append({"id": "07", "input": "%d\n%s\n" % (n, " ".join(words))})

    # 大数据：只含一个字母，最多 26 个分组
    n = 200000
    words = [rng.choice(LETTERS) for _ in range(n)]
    out.append({"id": "08", "input": "%d\n%s\n" % (n, " ".join(words))})

    # 大数据：长度 10，字母表只有 8 个符号，分组数约两万
    n = 200000
    words = ["".join(rng.choice("abcdefgh") for _ in range(10)) for _ in range(n)]
    out.append({"id": "09", "input": "%d\n%s\n" % (n, " ".join(words))})

    # 大数据：长度 10，全字母表，绝大多数单词各自成组
    n = 200000
    words = ["".join(rng.choice(LETTERS) for _ in range(10)) for _ in range(n)]
    out.append({"id": "10", "input": "%d\n%s\n" % (n, " ".join(words))})

    # 大数据：每个单词都相同
    n = 200000
    words = ["aabbbcccdd"] * n
    out.append({"id": "11", "input": "%d\n%s\n" % (n, " ".join(words))})
    return out
