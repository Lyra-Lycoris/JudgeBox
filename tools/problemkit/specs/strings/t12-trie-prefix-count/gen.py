import random


def cases():
    rng = random.Random(20261205)
    out = [
        {"id": "01", "input": "4\na ab abc b\n3\na ab d\n"},
        {"id": "02", "input": "1\nabc\n1\nabc\n"},
        {"id": "03", "input": "1\nabc\n1\nabcd\n"},
        {"id": "04", "input": "3\naaa aaa aaa\n4\na aa aaa aaaa\n"},
        {"id": "05", "input": "3\nb a ab\n4\na b ab c\n"},
    ]

    # 大数据：两个长单词，前缀几乎相同，询问正好等于较长的那个
    longA = "a" * 100000
    longB = "a" * 99999 + "b"
    out.append({"id": "06", "input": "2\n%s %s\n1\n%s\n" % (longA, longB, longA)})

    # 中等规模：二元字母表的随机单词与询问
    n = 1000
    words = ["".join(rng.choice("ab") for _ in range(8)) for _ in range(n)]
    q = 1000
    queries = ["".join(rng.choice("ab") for _ in range(4)) for _ in range(q)]
    out.append({"id": "07", "input": "%d\n%s\n%d\n%s\n" % (n, " ".join(words), q, " ".join(queries))})

    # 大数据：100000 个长度为 2 的单词，100000 个长度为 2 的询问
    n = 100000
    words = ["".join(rng.choice("ab") for _ in range(2)) for _ in range(n)]
    q = 100000
    queries = ["".join(rng.choice("ab") for _ in range(2)) for _ in range(q)]
    out.append({"id": "08", "input": "%d\n%s\n%d\n%s\n" % (n, " ".join(words), q, " ".join(queries))})

    # 大数据：单个超长单词，200000 个单字符询问
    word = "a" * 200000
    q = 200000
    out.append({"id": "09", "input": "1\n%s\n%d\n%s\n" % (word, q, " ".join(["a"] * q))})

    # 大数据：50000 个长度 4 的单词，50000 个长度 3 的询问
    n = 50000
    words = ["".join(rng.choice("ab") for _ in range(4)) for _ in range(n)]
    q = 50000
    queries = ["".join(rng.choice("ab") for _ in range(3)) for _ in range(q)]
    out.append({"id": "10", "input": "%d\n%s\n%d\n%s\n" % (n, " ".join(words), q, " ".join(queries))})
    return out
