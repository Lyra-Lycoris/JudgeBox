def solve(n: int, a: list[int], k: int) -> int:
    lo, hi = max(a), sum(a)
    while lo < hi:
        mid = (lo + hi) // 2
        parts = 1
        cur = 0
        for x in a:
            if cur + x > mid:
                parts += 1
                cur = x
                if parts > k:
                    break
            else:
                cur += x
        if parts <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
