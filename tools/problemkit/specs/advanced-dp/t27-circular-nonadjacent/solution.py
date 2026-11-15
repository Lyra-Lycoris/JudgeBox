def solve(n: int, a: list[int]) -> int:
    N = n
    if N == 1:
        return a[0] if a[0] > 0 else 0

    def linear(lo: int, hi: int) -> int:
        # 闭区间 lo..hi 上的线性「不相邻取和」，允许空集
        p2 = 0
        p1 = 0
        for i in range(lo, hi + 1):
            cur = p1
            cand = p2 + a[i]
            if cand > cur:
                cur = cand
            p2 = p1
            p1 = cur
        return p1

    r1 = linear(0, N - 2)
    r2 = linear(1, N - 1)
    return r1 if r1 > r2 else r2
