def solve(n: int, k: int, a: list[int]) -> int:
    pre = [0] * (n + 1)
    s = 0
    for i in range(n):
        s += a[i]
        pre[i + 1] = s
    lo, hi = -10 ** 12 - 1, 10 ** 12
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        best = 0
        feasible = False
        for j in range(k, n + 1):
            i = j - k
            candidate = pre[i] * 1000 - mid * i
            if candidate < best:
                best = candidate
            if pre[j] * 1000 - mid * j >= best:
                feasible = True
                break
        if feasible:
            lo = mid
        else:
            hi = mid
    return lo
