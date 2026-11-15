def solve(n: int, m: int, s: int, e: list[list[int]]) -> bool:
    INF = 10 ** 18
    dist = [INF] * (n + 1)
    dist[s] = 0
    for _ in range(n):
        changed = False
        for u, v, w in e:
            du = dist[u]
            if du < INF and du + w < dist[v]:
                dist[v] = du + w
                changed = True
        if not changed:
            return False
    return True
