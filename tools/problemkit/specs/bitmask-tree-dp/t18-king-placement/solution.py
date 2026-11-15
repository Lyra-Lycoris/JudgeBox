def solve(n: int, m: int) -> int:
    if n < m:
        n, m = m, n
    size = 1 << m
    valid = [x for x in range(size) if (x & (x << 1)) == 0]
    dp = [0] * size
    for x in valid:
        dp[x] = 1
    for _ in range(n - 1):
        ndp = [0] * size
        for a in valid:
            total = 0
            for b in valid:
                if (a & b) == 0 and (a & (b << 1)) == 0 and ((a << 1) & b) == 0:
                    total += dp[b]
            ndp[a] = total
        dp = ndp
    return sum(dp[x] for x in valid)
