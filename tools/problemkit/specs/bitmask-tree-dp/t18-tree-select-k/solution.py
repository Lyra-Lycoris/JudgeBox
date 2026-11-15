def solve(n: int, k: int, w: list[int], p: list[int]) -> int:
    NEG = -(1 << 62)
    dp = [[NEG] * (k + 1) for _ in range(n + 1)]
    sz = [1] * (n + 1)
    for i in range(1, n + 1):
        dp[i][0] = 0
        dp[i][1] = w[i - 1]
    for i in range(n, 1, -1):
        par = p[i - 2]
        dpv = dp[par]
        dpi = dp[i]
        si = sz[i] if sz[i] < k else k
        sv = sz[par] if sz[par] < k else k
        lim = si + sv
        if lim > k:
            lim = k
        for j in range(lim, 0, -1):
            best = dpv[j]
            lo = j - sv
            if lo < 1:
                lo = 1
            hi = j - 1
            if hi > si:
                hi = si
            t = lo
            while t <= hi:
                a = dpv[j - t]
                b = dpi[t]
                if a != NEG and b != NEG:
                    val = a + b
                    if val > best:
                        best = val
                t += 1
            dpv[j] = best
        sz[par] += sz[i]
    return dp[1][k]
