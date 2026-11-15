def solve(n: int, m: int, g: list[list[int]]) -> int:
    MOD = 1000000007
    dp = [0] * m
    for i in range(n):
        for j in range(m):
            if g[i][j] == 1:
                dp[j] = 0
            elif i == 0 and j == 0:
                dp[j] = 1
            else:
                left = dp[j - 1] if j > 0 else 0
                dp[j] = (dp[j] + left) % MOD
    return dp[m - 1]
