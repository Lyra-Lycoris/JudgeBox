def solve(x: int) -> int:
    lo, hi = 0, 1000000001
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        t = 2 * mid - 1
        if t * t <= 4 * x * 1000000:
            lo = mid
        else:
            hi = mid
    return lo
