def solve(n: int, target: int, coins: list[int]) -> int:
    MOD = 1000000007
    dp = [0] * (target + 1)
    dp[0] = 1
    for i in range(n):
        c = coins[i]
        if c > target:
            continue
        for j in range(c, target + 1):
            dp[j] = (dp[j] + dp[j - c]) % MOD
    return dp[target]
