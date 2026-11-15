from math import gcd


def solve(n: int, k: int, a: list[int]) -> str:
    cur = sum(a[:k])
    best = cur
    for i in range(k, n):
        cur += a[i] - a[i - k]
        if cur > best:
            best = cur
    g = gcd(abs(best), k)
    return "%d/%d" % (best // g, k // g)
