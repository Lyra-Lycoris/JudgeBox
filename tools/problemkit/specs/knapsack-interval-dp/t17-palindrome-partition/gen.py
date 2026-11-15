import random


def cases():
    rng = random.Random(20261120)
    out = []

    # 01 样例
    out.append({"id": "01", "input": "aab\n"})

    # 02 只有一个字符
    out.append({"id": "02", "input": "a\n"})

    # 03 两个不同字符
    out.append({"id": "03", "input": "ab\n"})

    # 04 1500 个相同字符：本身就是回文
    out.append({"id": "04", "input": "a" * 1500 + "\n"})

    # 05 大数据：只有两种字符的随机串
    out.append({"id": "05", "input": "".join(rng.choice("ab") for _ in range(1500)) + "\n"})

    # 06 本身是回文
    out.append({"id": "06", "input": "abacaba\n"})

    # 07 大数据：26 种字符的随机串，答案接近 n - 1
    out.append({"id": "07", "input": "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(1500)) + "\n"})

    # 08 重复的偶数回文块
    out.append({"id": "08", "input": "abcbaabcba\n"})

    # 09 交替串
    out.append({"id": "09", "input": "ab" * 750 + "\n"})

    # 10 两个相同字符
    out.append({"id": "10", "input": "aa\n"})

    # 11 中等规模随机
    out.append({"id": "11", "input": "".join(rng.choice("abcd") for _ in range(300)) + "\n"})

    # 12 重复块 "aabb"
    out.append({"id": "12", "input": "aabb" * 375 + "\n"})

    return out
