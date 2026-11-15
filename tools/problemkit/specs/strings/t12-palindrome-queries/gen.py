import random

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def random_ranges(rng, n, q):
    ranges = []
    for _ in range(q):
        left = rng.randint(1, n)
        right = rng.randint(left, n)
        ranges.append((left, right))
    return ranges


def format_ranges(ranges):
    return "\n".join("%d %d" % pair for pair in ranges)


def cases():
    rng = random.Random(20261206)
    out = [
        {"id": "01", "input": "5\nabcba\n3\n1 5\n1 3\n2 4\n"},
        {"id": "02", "input": "1\na\n1\n1 1\n"},
        {"id": "03", "input": "4\nabba\n4\n1 4\n2 3\n1 2\n3 4\n"},
        {"id": "04", "input": "6\naaaaaa\n3\n1 6\n2 5\n3 3\n"},
        {"id": "05", "input": "2\nab\n3\n1 1\n2 2\n1 2\n"},
    ]

    # 中等规模：二元字母表的随机串
    n = 2000
    s = "".join(rng.choice("ab") for _ in range(n))
    ranges = random_ranges(rng, n, 2000)
    out.append({"id": "06", "input": "%d\n%s\n%d\n%s\n" % (n, s, len(ranges), format_ranges(ranges))})

    # 大数据：26 字母随机串，几乎全部询问答案为 0
    n = 200000
    s = "".join(rng.choice(LETTERS) for _ in range(n))
    ranges = random_ranges(rng, n, 200000)
    out.append({"id": "07", "input": "%d\n%s\n%d\n%s\n" % (n, s, len(ranges), format_ranges(ranges))})

    # 大数据：整体是回文（后半段是前半段的翻转）
    half = 100000
    n = 2 * half
    left = "".join(rng.choice(LETTERS) for _ in range(half))
    s = left + left[::-1]
    ranges = random_ranges(rng, n, 200000)
    out.append({"id": "08", "input": "%d\n%s\n%d\n%s\n" % (n, s, len(ranges), format_ranges(ranges))})

    # 大数据：全是同一个字符，答案全为 1
    n = 200000
    s = "a" * n
    ranges = random_ranges(rng, n, 200000)
    out.append({"id": "09", "input": "%d\n%s\n%d\n%s\n" % (n, s, len(ranges), format_ranges(ranges))})

    # 大数据：二元字母表随机串，答案 0/1 混合
    n = 200000
    s = "".join(rng.choice("ab") for _ in range(n))
    ranges = random_ranges(rng, n, 200000)
    out.append({"id": "10", "input": "%d\n%s\n%d\n%s\n" % (n, s, len(ranges), format_ranges(ranges))})
    return out
