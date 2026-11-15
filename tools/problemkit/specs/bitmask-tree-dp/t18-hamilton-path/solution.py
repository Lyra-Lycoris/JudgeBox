def solve(n: int, w: list[list[int]]) -> int:
    INF = 1 << 62
    if n == 1:
        return 0
    size = 1 << n
    full = size - 1
    dp = [[INF] * n for _ in range(size)]
    dp[1][0] = 0
    for mask in range(1, size, 2):
        row = dp[mask]
        rest = full ^ mask
        for v in range(n):
            cur = row[v]
            if cur == INF:
                continue
            wv = w[v]
            nv = rest
            while nv:
                b = nv & -nv
                u = b.bit_length() - 1
                nv ^= b
                val = cur + wv[u]
                nm = mask | b
                if val < dp[nm][u]:
                    dp[nm][u] = val
    return dp[full][n - 1]
