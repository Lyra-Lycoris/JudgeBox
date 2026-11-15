def solve(n: int, cap: int, w: list[int], v: list[int]) -> int:
    dp = [0] * (cap + 1)
    for i in range(n):
        wi = w[i]
        if wi > cap:
            continue
        vi = v[i]
        for j in range(cap, wi - 1, -1):
            cand = dp[j - wi] + vi
            if cand > dp[j]:
                dp[j] = cand
    return dp[cap]
