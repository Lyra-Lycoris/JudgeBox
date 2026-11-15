def solve(n: int, p: list[int]) -> list[int]:
    N = n
    down = [0] * (N + 1)
    up = [0] * (N + 1)
    best1 = [0] * (N + 1)
    best2 = [0] * (N + 1)
    who = [0] * (N + 1)
    for i in range(N, 1, -1):
        par = p[i - 2]
        val = down[i] + 1
        if val > best1[par]:
            best2[par] = best1[par]
            best1[par] = val
            who[par] = i
        elif val > best2[par]:
            best2[par] = val
        if val > down[par]:
            down[par] = val
    for i in range(2, N + 1):
        par = p[i - 2]
        sib = best1[par] if who[par] != i else best2[par]
        base = up[par] if up[par] > sib else sib
        up[i] = base + 1
    ans = [0] * N
    for i in range(1, N + 1):
        ans[i - 1] = down[i] if down[i] > up[i] else up[i]
    return ans
