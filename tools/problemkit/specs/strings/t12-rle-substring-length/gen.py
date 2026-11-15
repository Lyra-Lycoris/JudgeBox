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
    rng = random.Random(20261207)
    out = [
        {"id": "01", "input": "6\naaabbc\n4\n1 6\n1 3\n4 6\n1 1\n"},
        {"id": "02", "input": "1\nz\n1\n1 1\n"},
        {"id": "03", "input": "12\naaaaaaaaaaaa\n4\n1 12\n1 9\n1 10\n5 12\n"},
        {"id": "04", "input": "5\nabcde\n3\n1 5\n2 4\n3 3\n"},
        {"id": "05", "input": "7\naabcccc\n4\n1 7\n1 2\n3 6\n7 7\n"},
    ]

    # 中等规模：三元字母表随机串，段较短
    n = 2000
    s = "".join(rng.choice("abc") for _ in range(n))
    ranges = random_ranges(rng, n, 2000)
    out.append({"id": "06", "input": "%d\n%s\n%d\n%s\n" % (n, s, len(ranges), format_ranges(ranges))})

    # 大数据：所有段长度都为 1，答案就是区间长度
    n = 200000
    s = "ab" * (n // 2)
    ranges = random_ranges(rng, n, 200000)
    out.append({"id": "07", "input": "%d\n%s\n%d\n%s\n" % (n, s, len(ranges), format_ranges(ranges))})

    # 大数据：整串只有一段，答案只依赖区间长度
    n = 200000
    s = "a" * n
    ranges = random_ranges(rng, n, 200000)
    out.append({"id": "08", "input": "%d\n%s\n%d\n%s\n" % (n, s, len(ranges), format_ranges(ranges))})

    # 大数据：26 字母随机串，段普遍很短
    n = 200000
    s = "".join(rng.choice(LETTERS) for _ in range(n))
    ranges = random_ranges(rng, n, 200000)
    out.append({"id": "09", "input": "%d\n%s\n%d\n%s\n" % (n, s, len(ranges), format_ranges(ranges))})

    # 大数据：每段长 100，边界处常被截断
    n = 200000
    s = ("a" * 100 + "b" * 100) * (n // 200)
    ranges = random_ranges(rng, n, 200000)
    out.append({"id": "10", "input": "%d\n%s\n%d\n%s\n" % (n, s, len(ranges), format_ranges(ranges))})

    # 大数据：段长为 9 与 11，跨越十进制位数变化的边界
    n = 200000
    s = ("a" * 9 + "b" * 11) * (n // 20)
    ranges = random_ranges(rng, n, 200000)
    out.append({"id": "11", "input": "%d\n%s\n%d\n%s\n" % (n, s, len(ranges), format_ranges(ranges))})
    return out
