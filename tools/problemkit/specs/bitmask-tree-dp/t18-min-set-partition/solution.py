def solve(n: int, c: list[int]) -> int:
    INF = 1 << 62
    size = 1 << n
    dp = [INF] * size
    dp[0] = 0
    for mask in range(1, size):
        low = mask & -mask
        rest = mask ^ low
        best = INF
        sub = rest
        while True:
            s = sub | low
            v = dp[mask ^ s] + c[s]
            if v < best:
                best = v
            if sub == 0:
                break
            sub = (sub - 1) & rest
        dp[mask] = best
    return dp[size - 1]
