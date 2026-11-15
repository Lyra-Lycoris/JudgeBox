import random


def _line(values):
    return " ".join(str(x) for x in values)


def _input(ops):
    parts = ["%d\n" % len(ops)]
    for op in ops:
        parts.append(_line(op) + "\n")
    return "".join(parts)


def _random_ops(rng, q, low, high, insert_p=0.4, erase_p=0.3):
    counts = {}
    touched = []
    ops = []
    size = 0
    for _ in range(q):
        r = rng.random()
        if r < insert_p or size == 0:
            v = rng.randint(low, high)
            if counts.get(v, 0) == 0:
                touched.append(v)
            counts[v] = counts.get(v, 0) + 1
            size += 1
            ops.append((1, v))
        elif r < insert_p + erase_p:
            v = None
            for _try in range(30):
                candidate = touched[rng.randrange(len(touched))]
                if counts.get(candidate, 0) > 0:
                    v = candidate
                    break
            if v is None:
                v = rng.randint(low, high)
                if counts.get(v, 0) == 0:
                    touched.append(v)
                counts[v] = counts.get(v, 0) + 1
                size += 1
                ops.append((1, v))
            else:
                counts[v] -= 1
                size -= 1
                ops.append((2, v))
        else:
            ops.append((3, rng.randint(1, size)))
    return ops


def cases():
    rng = random.Random(20261126)
    big = 1000000000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input([(1, 5), (1, 3), (1, 9),
                                             (3, 1), (3, 3), (2, 3), (3, 1)])})

    # 02 边界：只有一个数
    out.append({"id": "02", "input": _input([(1, 42), (3, 1), (3, 1), (2, 42)])})

    # 03 边界：全部相同
    out.append({"id": "03", "input": _input([(1, 7), (1, 7), (1, 7),
                                             (3, 1), (3, 2), (3, 3), (2, 7), (3, 2)])})

    # 04 极值：最小与最大
    out.append({"id": "04", "input": _input([(1, 1), (1, big), (3, 1), (3, 2),
                                             (2, 1), (3, 1), (1, 1), (3, 1)])})

    # 05 小数据：大量重复与删除
    out.append({"id": "05", "input": _input([(1, 2), (1, 1), (1, 2), (3, 1), (3, 2),
                                             (3, 3), (2, 1), (3, 1), (2, 2), (3, 1),
                                             (2, 2), (1, 3), (3, 1)])})

    # 06 中等随机：值域很小，重复很多
    ops = _random_ops(rng, 2000, 1, 5)
    ops.append((3, 1))
    out.append({"id": "06", "input": _input(ops)})

    # 07 大数据：q = 100000，值域 1e9
    ops = _random_ops(rng, 100000, 1, big)
    ops.append((3, 1))
    out.append({"id": "07", "input": _input(ops)})

    # 08 大数据：先插入 70000 个，再查询 70000 次，最后删除 60000 个
    ops = []
    for i in range(70000):
        ops.append((1, rng.randint(1, big)))
    for _ in range(70000):
        ops.append((3, rng.randint(1, 70000)))
    for i in range(60000):
        ops.append((2, ops[i][1]))
    out.append({"id": "08", "input": _input(ops)})

    # 09 大数据：值域只有 3 种取值
    ops = _random_ops(rng, 100000, 1, 3)
    ops.append((3, 1))
    out.append({"id": "09", "input": _input(ops)})

    return out
