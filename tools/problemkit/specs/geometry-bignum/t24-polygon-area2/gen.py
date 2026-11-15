import math
import random

LIMIT = 10 ** 6


def _lines(values):
    return " ".join(str(v) for v in values)


def _ring(n, rmin, rmax, rng, reverse=False):
    """按极角排序生成一个简单多边形（星形），坐标绝对值不超过 LIMIT。"""
    points = []
    seen = set()
    step = 2.0 * math.pi / n
    for k in range(n):
        theta = step * (k + rng.uniform(-0.35, 0.35))
        r = rng.randint(rmin, rmax)
        x = int(round(r * math.cos(theta)))
        y = int(round(r * math.sin(theta)))
        while (x, y) in seen:
            x += 1
        seen.add((x, y))
        points.append((x, y))
    if reverse:
        points.reverse()
    return points


def _polygon(points):
    return "%d\n%s\n%s\n" % (len(points),
                             _lines([p[0] for p in points]),
                             _lines([p[1] for p in points]))


def cases():
    rng = random.Random(20261117)
    out = []

    # 01 样例：直角三角形 (0,0),(4,0),(0,3)，2S = 12
    out.append({"id": "01", "input": _polygon([(0, 0), (4, 0), (0, 3)])})

    # 02 三个顶点全部重合，面积 0
    out.append({"id": "02", "input": _polygon([(5, -5), (5, -5), (5, -5)])})

    # 03 三点共线，面积 0
    out.append({"id": "03", "input": _polygon([(0, 0), (1, 1), (2, 2)])})

    # 04 极值正方形，2S = 8 * 10^12
    out.append({"id": "04", "input": _polygon([(-LIMIT, -LIMIT), (LIMIT, -LIMIT), (LIMIT, LIMIT), (-LIMIT, LIMIT)])})

    # 05 凹多边形（箭头形）
    out.append({"id": "05", "input": _polygon([(0, 0), (4, 0), (4, 4), (2, 2), (0, 4)])})

    # 06 中等规模，径向多边形
    out.append({"id": "06", "input": _polygon(_ring(1000, 100000, LIMIT, rng))})

    # 07 大规模，接近圆周的凸多边形
    out.append({"id": "07", "input": _polygon(_ring(200000, 800000, LIMIT, rng))})

    # 08 同样的大规模多边形，但顶点逆序给出
    out.append({"id": "08", "input": _polygon(_ring(200000, 800000, LIMIT, rng, reverse=True))})

    # 09 极值三角形，2S = 4 * 10^12
    out.append({"id": "09", "input": _polygon([(-LIMIT, -LIMIT), (LIMIT, -LIMIT), (0, LIMIT)])})

    # 10 大规模星形多边形，面积较小但跨度很大
    out.append({"id": "10", "input": _polygon(_ring(200000, 100000, LIMIT, rng))})
    return out
