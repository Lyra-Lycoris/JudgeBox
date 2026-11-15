import math
import random

LIMIT = 10 ** 9


def _line(values):
    return " ".join(str(v) for v in values)


def _pack(points):
    return "%d\n%s\n%s\n" % (len(points),
                             _line([p[0] for p in points]),
                             _line([p[1] for p in points]))


def _ring(n, rmin, rmax, rng):
    points = []
    seen = set()
    step = 2.0 * math.pi / n
    for k in range(n):
        theta = step * (k + rng.uniform(-0.3, 0.3))
        r = rng.randint(rmin, rmax)
        x = int(round(r * math.cos(theta)))
        y = int(round(r * math.sin(theta)))
        while (x, y) in seen:
            x += 1
        seen.add((x, y))
        points.append((x, y))
    return points


def _square_boundary(per_edge, half):
    points = []
    step = (2 * half) // per_edge
    for k in range(per_edge):
        points.append((-half + k * step, -half))
    for k in range(per_edge):
        points.append((half, -half + k * step))
    for k in range(per_edge):
        points.append((half - k * step, half))
    for k in range(per_edge):
        points.append((-half, half - k * step))
    return points


def cases():
    rng = random.Random(20261119)
    out = []

    # 01 样例：正方形四个角 + 两个内点，凸包 4 个顶点
    out.append({"id": "01", "input": _pack([(0, 0), (4, 0), (4, 4), (0, 4), (2, 2), (1, 1)])})

    # 02 只有一个点
    out.append({"id": "02", "input": _pack([(-LIMIT, LIMIT)])})

    # 03 只有两个不同的点
    out.append({"id": "03", "input": _pack([(-3, 2), (7, -8)])})

    # 04 十万个相同的点
    out.append({"id": "04", "input": _pack([(0, 0)] * 100000)})

    # 05 十万个共线的点
    out.append({"id": "05", "input": _pack([(i, 2 * i) for i in range(100000)])})

    # 06 极值正方形 + 中心点
    out.append({"id": "06", "input": _pack([(-LIMIT, -LIMIT), (LIMIT, -LIMIT), (LIMIT, LIMIT), (-LIMIT, LIMIT), (0, 0)])})

    # 07 中等规模随机
    out.append({"id": "07", "input": _pack([(rng.randint(-1000, 1000), rng.randint(-1000, 1000)) for _ in range(1000)])})

    # 08 大规模随机
    out.append({"id": "08", "input": _pack([(rng.randint(-LIMIT // 1000, LIMIT // 1000), rng.randint(-LIMIT // 1000, LIMIT // 1000)) for _ in range(200000)])})

    # 09 大规模近似圆周上的点
    out.append({"id": "09", "input": _pack(_ring(200000, 999000, LIMIT // 1000, rng))})

    # 10 大规模：全部落在正方形边界上，凸包只有 4 个顶点
    out.append({"id": "10", "input": _pack(_square_boundary(50000, LIMIT // 1000))})
    return out
