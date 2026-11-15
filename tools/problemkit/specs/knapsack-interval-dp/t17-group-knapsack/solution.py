def solve(n: int, cap: int, g: list[int], w: list[int], v: list[int]) -> int:
    groups = [[] for _ in range(n + 2)]
    for i in range(n):
        groups[g[i]].append(i)
    dp = [0] * (cap + 1)
    for key in range(1, n + 1):
        if not groups[key]:
            continue
        ndp = dp[:]
        for idx in groups[key]:
            wi = w[idx]
            if wi > cap:
                continue
            vi = v[idx]
            for j in range(cap, wi - 1, -1):
                cand = dp[j - wi] + vi
                if cand > ndp[j]:
                    ndp[j] = cand
        dp = ndp
    return dp[cap]
