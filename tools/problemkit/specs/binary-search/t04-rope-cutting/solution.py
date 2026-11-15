def solve(n: int, a: list[int], k: int) -> int:
    lo, hi = 0, max(a)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        cnt = 0
        for x in a:
            cnt += x // mid
            if cnt >= k:
                break
        if cnt >= k:
            lo = mid
        else:
            hi = mid - 1
    return lo
