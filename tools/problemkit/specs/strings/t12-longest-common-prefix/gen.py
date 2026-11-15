import random

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def cases():
    rng = random.Random(20261204)
    out = [
        {"id": "01", "input": "3\nflower flow flight\n"},
        {"id": "02", "input": "1\nabc\n"},
        {"id": "03", "input": "2\nabc abd\n"},
        {"id": "04", "input": "3\nabc def ghi\n"},
        {"id": "05", "input": "4\naaa aaa aaa aaa\n"},
        {"id": "06", "input": "2\na ab\n"},
        {"id": "07", "input": "2\nab a\n"},
    ]

    # 中等规模：1000 个字符串，前 4 个字符固定相同
    k = 1000
    words = ["abcd" + "".join(rng.choice(LETTERS) for _ in range(6)) for _ in range(k)]
    out.append({"id": "08", "input": "%d\n%s\n" % (k, " ".join(words))})

    # 大数据：200000 个长度为 1 的字符串，全部为 a
    k = 200000
    out.append({"id": "09", "input": "%d\n%s\n" % (k, " ".join(["a"] * k))})

    # 大数据：只有两个字符串，各长 100000，公共前缀长 99999
    half = 100000
    prefix = "".join(rng.choice(LETTERS) for _ in range(half - 1))
    first = prefix + "a"
    second = prefix + "b"
    out.append({"id": "10", "input": "2\n%s %s\n" % (first, second)})

    # 大数据：100000 个长度为 2 的相同字符串
    k = 100000
    out.append({"id": "11", "input": "%d\n%s\n" % (k, " ".join(["ab"] * k))})

    # 大数据：100000 个长度为 2 的字符串，首字符就不同，公共前缀为 0
    k = 100000
    words = ["aa"] * k
    words[1] = "ba"
    out.append({"id": "12", "input": "%d\n%s\n" % (k, " ".join(words))})
    return out
