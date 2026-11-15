def solve(n: int, a: list[int], k: int) -> int:
    if k <= 1:
        return 0
    b = sorted(a)
    lo = 0
    hi = (b[-1] - b[0]) // (k - 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        cnt = 1
        last = b[0]
        for i in range(1, n):
            if b[i] - last >= mid:
                cnt += 1
                last = b[i]
                if cnt >= k:
                    break
        if cnt >= k:
            lo = mid
        else:
            hi = mid - 1
    return lo
