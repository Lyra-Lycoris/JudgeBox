def solve(n: int, k: int, a: list[int]) -> int:
    total = 0
    for x in a:
        total += x
    lo, hi = 0, total // k
    while lo < hi:
        mid = (lo + hi + 1) // 2
        cnt = 0
        cur = 0
        for x in a:
            cur += x
            if cur >= mid:
                cnt += 1
                cur = 0
                if cnt >= k:
                    break
        if cnt >= k:
            lo = mid
        else:
            hi = mid - 1
    return lo
