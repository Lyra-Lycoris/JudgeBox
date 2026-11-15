import math
import random

LOG10_E = 0.4342944819032518
TWO_PI = 6.283185307179586
LN10 = 2.302585092994046

# floor(log10(n!)) 距离整数至少 10^-3 的 n 才收录，保证各语言浮点结果一致。
MARGIN = 1e-3


def _log10_factorial(n):
    """Stirling 级数给出的 log10(n!) 近似值。"""
    fn = float(n)
    return (fn * math.log10(fn)
            - fn * LOG10_E
            + 0.5 * math.log10(TWO_PI * fn)
            + 1.0 / (12.0 * fn * LN10))


def _safe(n):
    if n <= 20:
        return True
    frac = _log10_factorial(n) % 1.0
    return MARGIN < frac < 1.0 - MARGIN


def _pick(rng, lo, hi, count):
    picked = []
    while len(picked) < count:
        n = rng.randint(lo, hi)
        if _safe(n):
            picked.append(n)
    return picked


def _case(values):
    return {"input": "%d\n%s\n" % (len(values), "\n".join(str(v) for v in values))}


def cases():
    rng = random.Random(20261122)
    out = []

    # 01 样例
    out.append(dict(id="01", **_case([1, 2, 5, 10, 20])))

    # 02 n = 1
    out.append(dict(id="02", **_case([1])))

    # 03 最大规模
    out.append(dict(id="03", **_case([1000000000])))

    # 04 精确公式与 Stirling 公式的交界附近，以及接近 10^9 的数
    out.append(dict(id="04", **_case([999999999, 21, 22, 1000000000])))

    # 05 中等规模随机
    out.append(dict(id="05", **_case(_pick(rng, 1, 1000000, 1000))))

    # 06 大数据：10^5 组全范围随机
    out.append(dict(id="06", **_case(_pick(rng, 1, 1000000000, 100000))))

    # 07 大数据：10^5 组小 n（走精确阶乘分支）
    out.append(dict(id="07", **_case([rng.randint(1, 20) for _ in range(100000)])))

    # 08 大数据：10^5 组接近 10^9 的 n
    out.append(dict(id="08", **_case(_pick(rng, 1000000000 - 1000, 1000000000, 100000))))

    # 09 大数据：10^5 组 10^6 到 10^9 的随机数
    out.append(dict(id="09", **_case(_pick(rng, 1000000, 1000000000, 100000))))

    # 10 几个特殊值
    out.append(dict(id="10", **_case([2, 3, 4, 6, 7, 8, 9, 11, 100, 1000])))
    return out
