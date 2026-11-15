import random

SEED = 20261114
LIMIT = 10 ** 9


def pack(ops, vals):
    return "%d\n%s\n%s\n" % (len(ops), " ".join(map(str, ops)), " ".join(map(str, vals)))


def random_case(rng, m, max_abs=LIMIT):
    ops, vals = [], []
    depth = 0
    queries = 0
    while len(ops) < m:
        left = m - len(ops)
        if depth == 0:
            choices = [1]
        elif left <= 1:
            choices = [3, 2] if queries > 0 else [3]
        else:
            choices = [1, 2, 3]
        kind = rng.choice(choices)
        if kind == 1:
            ops.append(1)
            vals.append(rng.randint(-max_abs, max_abs))
            depth += 1
        elif kind == 2:
            ops.append(2)
            vals.append(0)
            depth -= 1
        else:
            ops.append(3)
            vals.append(0)
            queries += 1
    if queries == 0:
        # 把最后一个弹出改成查询，保证至少有一次查询且操作仍然合法
        index = len(ops) - 1
        for i in range(len(ops) - 1, -1, -1):
            if ops[i] == 2:
                index = i
                break
        ops[index] = 3
        vals[index] = 0
    return ops, vals


def cases():
    rng = random.Random(SEED)
    out = [
        {"id": "01", "input": "6\n1 1 3 2 3 3\n5 -3 0 0 0 0\n"},
        {"id": "02", "input": "4\n1 1 3 2\n2 2 0 0\n"},
    ]

    # 单次压入后立刻查询
    out.append({"id": "03", "input": pack([1, 3], [0, 0])})

    # 全部元素相同
    ops = [1] * 5 + [3] * 5
    vals = [7] * 5 + [0] * 5
    out.append({"id": "04", "input": pack(ops, vals)})

    # 极值与负数
    ops = [1, 1, 3, 2, 3, 1, 3, 2, 3]
    vals = [LIMIT, -LIMIT, 0, 0, 0, -LIMIT, 0, 0, 0]
    out.append({"id": "05", "input": pack(ops, vals)})

    # 随机中等规模
    ops, vals = random_case(rng, 1000)
    out.append({"id": "06", "input": pack(ops, vals)})

    # 随机大规模
    ops, vals = random_case(rng, 200000)
    out.append({"id": "07", "input": pack(ops, vals)})

    # 先压入 100000 个递增元素，再查询 100000 次
    ops = [1] * 100000 + [3] * 100000
    vals = [i * 10000 for i in range(100000)] + [0] * 100000
    out.append({"id": "08", "input": pack(ops, vals)})

    # 先压入 99999 个元素，查询一次，再全部弹出
    ops = [1] * 99999 + [3] + [2] * 99999
    vals = [LIMIT - i for i in range(99999)] + [0] + [0] * 99999
    out.append({"id": "09", "input": pack(ops, vals)})

    # 大量重复值
    ops = [1] * 100000 + [3] * 100000
    vals = [0] * 100000 + [0] * 100000
    out.append({"id": "10", "input": pack(ops, vals)})

    return out
