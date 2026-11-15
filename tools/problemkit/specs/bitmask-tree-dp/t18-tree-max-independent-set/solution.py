def solve(n: int, w: list[int], p: list[int]) -> int:
    dp0 = [0] * (n + 1)
    dp1 = [0] * (n + 1)
    for i in range(1, n + 1):
        dp1[i] = w[i - 1]
    for i in range(n, 1, -1):
        par = p[i - 2]
        a = dp0[i]
        b = dp1[i]
        dp0[par] += a if a > b else b
        dp1[par] += a
    return dp0[1] if dp0[1] > dp1[1] else dp1[1]
