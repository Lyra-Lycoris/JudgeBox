def solve(n: int, s: str) -> int:
    MOD = 1000000007
    length = min(n, len(s))
    if length <= 0:
        return 0
    dp = [0] * (length + 1)
    dp[0] = 1
    last = [-1] * 26
    for i in range(1, length + 1):
        c = ord(s[i - 1]) - 97
        value = 2 * dp[i - 1] % MOD
        if last[c] >= 0:
            value = (value - dp[last[c]] + MOD) % MOD
        dp[i] = value
        last[c] = i - 1
    return (dp[length] - 1 + MOD) % MOD
