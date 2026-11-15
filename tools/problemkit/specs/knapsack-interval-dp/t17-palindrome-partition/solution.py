def solve(s: str) -> int:
    n = len(s)
    if n <= 1:
        return 0
    dp = [n + 1] * (n + 1)
    dp[0] = 0
    for c in range(n):
        l, r = c, c
        while l >= 0 and r < n and s[l] == s[r]:
            if dp[l] + 1 < dp[r + 1]:
                dp[r + 1] = dp[l] + 1
            l -= 1
            r += 1
        l, r = c, c + 1
        while l >= 0 and r < n and s[l] == s[r]:
            if dp[l] + 1 < dp[r + 1]:
                dp[r + 1] = dp[l] + 1
            l -= 1
            r += 1
    return dp[n] - 1
