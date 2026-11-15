def solve(n: int, a: list[int]) -> int:
    if n <= 1:
        return 0
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            best = -1
            for k in range(i, j):
                cand = dp[i][k] + dp[k + 1][j]
                if best < 0 or cand < best:
                    best = cand
            dp[i][j] = best + pre[j + 1] - pre[i]
    return dp[0][n - 1]
