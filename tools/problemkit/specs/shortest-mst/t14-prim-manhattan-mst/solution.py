def solve(n: int, p: list[list[int]]) -> int:
    xs = [p[i][0] for i in range(n)]
    ys = [p[i][1] for i in range(n)]
    INF = 10 ** 30
    best = [INF] * n
    used = bytearray(n)
    best[0] = 0
    total = 0
    for _ in range(n):
        u = -1
        bd = INF
        for i in range(n):
            if not used[i] and best[i] < bd:
                bd = best[i]
                u = i
        used[u] = 1
        total += bd
        xu = xs[u]
        yu = ys[u]
        for i in range(n):
            if used[i]:
                continue
            d = abs(xs[i] - xu) + abs(ys[i] - yu)
            if d < best[i]:
                best[i] = d
    return total
