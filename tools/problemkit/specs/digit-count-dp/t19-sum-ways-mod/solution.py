def solve(n: int, m: int) -> int:
    MOD = 1000000007
    if n <= 0:
        return 1
    if m > n:
        m = n
    dp = [0] * (n + 1)
    dp[0] = 1
    window = 1
    for i in range(1, n + 1):
        dp[i] = window
        sub = dp[i - m] if i >= m else 0
        window = (window + dp[i] - sub) % MOD
    return dp[n]
