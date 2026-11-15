def solve(n: int, p: list[int]) -> list[int]:
    sz = [1] * (n + 1)
    for i in range(n, 1, -1):
        sz[p[i - 2]] += sz[i]
    depth = [0] * (n + 1)
    f = [0] * (n + 1)
    for i in range(2, n + 1):
        depth[i] = depth[p[i - 2]] + 1
        f[1] += depth[i]
    for i in range(2, n + 1):
        f[i] = f[p[i - 2]] + n - 2 * sz[i]
    return f[1:]
