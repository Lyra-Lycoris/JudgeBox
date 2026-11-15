import random


def _line(values):
    return " ".join(str(v) for v in values)


def cases():
    rng = random.Random(20261116)
    out = []

    # 01 样例：1^2 = 3，1^3 = 2，2^3 = 1
    out.append({"id": "01", "input": "3\n1 2 3\n"})

    # 02 边界 n = 1，没有数对，答案为 0
    out.append({"id": "02", "input": "1\n123456789\n"})

    # 03 边界 n = 2，两个数相同
    out.append({"id": "03", "input": "2\n5 5\n"})

    # 04 全部相同
    out.append({"id": "04", "input": "2000\n%s\n" % _line([131072] * 2000)})

    # 05 大量 0 与一个最大值 10^9
    zeros = [0] * 1999 + [10 ** 9]
    rng.shuffle(zeros)
    out.append({"id": "05", "input": "2000\n%s\n" % _line(zeros)})

    # 06 小范围随机：异或结果都很小
    out.append({"id": "06", "input": "2000\n%s\n" % _line([rng.randint(0, 1023) for _ in range(2000)])})

    # 07 全范围随机
    out.append({"id": "07", "input": "2000\n%s\n" % _line([rng.randint(0, 10 ** 9) for _ in range(2000)])})

    # 08 只有 0 和 10^9，最大异或对为该值
    out.append({"id": "08", "input": "2000\n%s\n" % _line([0, 10 ** 9] * 1000)})

    # 09 最坏情况：2000 个互不相同的伪随机数
    out.append({"id": "09", "input": "2000\n%s\n" % _line([(i * 2654435761) % (10 ** 9 + 1) for i in range(2000)])})

    # 10 奇数长度 n = 1999 的随机数据
    out.append({"id": "10", "input": "1999\n%s\n" % _line([rng.randint(0, 10 ** 9) for _ in range(1999)])})

    return out
