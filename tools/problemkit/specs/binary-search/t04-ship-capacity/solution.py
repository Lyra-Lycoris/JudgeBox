def solve(n: int, w: list[int], d: int) -> int:
    lo, hi = max(w), sum(w)
    while lo < hi:
        mid = (lo + hi) // 2
        days = 1
        cur = 0
        for x in w:
            if cur + x > mid:
                days += 1
                cur = x
                if days > d:
                    break
            else:
                cur += x
        if days <= d:
            hi = mid
        else:
            lo = mid + 1
    return lo
