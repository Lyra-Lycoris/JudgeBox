def solve(n: int, p: list[int]) -> int:
    dp0 = [0] * (n + 1)
    dp1 = [1] * (n + 1)
    for i in range(n, 1, -1):
        par = p[i - 2]
        dp0[par] += dp1[i]
        dp1[par] += dp0[i] if dp0[i] < dp1[i] else dp1[i]
    return dp0[1] if dp0[1] < dp1[1] else dp1[1]
