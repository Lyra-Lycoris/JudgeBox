def solve(n: int, e: list[int]) -> int:
    if n <= 1:
        return 0
    g = [[] for _ in range(n + 1)]
    for i in range(0, len(e), 2):
        u = e[i]
        v = e[i + 1]
        g[u].append(v)
        g[v].append(u)

    def bfs(src):
        dist = [-1] * (n + 1)
        dist[src] = 0
        q = [src]
        for u in q:
            du = dist[u] + 1
            for v in g[u]:
                if dist[v] < 0:
                    dist[v] = du
                    q.append(v)
        far = src
        best = 0
        for i in range(1, n + 1):
            if dist[i] > best:
                best = dist[i]
                far = i
        return far, best

    a, _ = bfs(1)
    _, diameter = bfs(a)
    return diameter
