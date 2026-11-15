import random


def _join(values):
    return " ".join(str(x) for x in values)


def _build(nums, ops):
    parts = ["%d" % len(nums), _join(nums)]
    if ops:
        parts.append(_join(ops))
    return "\n".join(parts) + "\n"


def cases():
    rng = random.Random(20261119)
    out = []

    # 01 样例
    out.append({"id": "01", "input": "3\n1 2 3\n+ *\n"})

    # 02 只有一个数字
    out.append({"id": "02", "input": "1\n7\n"})

    # 03 全是 0
    out.append({"id": "03", "input": _build([0] * 10, ["*", "+", "*", "-", "+", "*", "-", "+", "*"])})

    # 04 大数据：15 个数字、随机运算符
    nums = [rng.randint(0, 9) for _ in range(15)]
    ops = [rng.choice(["+", "-", "*"]) for _ in range(14)]
    out.append({"id": "04", "input": _build(nums, ops)})

    # 05 全是加法
    out.append({"id": "05", "input": _build([9] * 15, ["+"] * 14)})

    # 06 全是乘法：9^15
    out.append({"id": "06", "input": _build([9] * 15, ["*"] * 14)})

    # 07 两个数字、一次减法
    out.append({"id": "07", "input": "2\n5 3\n-\n"})

    # 08 含 0 的减法
    out.append({"id": "08", "input": _build([9, 0, 9, 0, 9], ["-", "-", "-", "-"])})

    # 09 随机中等：12 个数字，多为减法
    nums = [rng.randint(0, 9) for _ in range(12)]
    ops = [rng.choice(["-", "-", "+"]) for _ in range(11)]
    out.append({"id": "09", "input": _build(nums, ops)})

    # 10 全是 1 和减法：最大值是 1
    out.append({"id": "10", "input": _build([1] * 14, ["-"] * 13)})

    # 11 含 0 的乘法
    nums = [rng.randint(0, 9) for _ in range(15)]
    ops = [rng.choice(["*", "*", "-"]) for _ in range(14)]
    out.append({"id": "11", "input": _build(nums, ops)})

    return out
