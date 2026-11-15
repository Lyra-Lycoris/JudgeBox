def solve(n: int, e: list[int]) -> int:
    if n == 1:
        return 1
    g = [[] for _ in range(n + 1)]
    for i in range(0, len(e), 2):
        u = e[i]
        v = e[i + 1]
        g[u].append(v)
        g[v].append(u)

    parent = [1] * (n + 1)
    visited = [False] * (n + 1)
    visited[1] = True
    order = [1]
    for u in order:
        for v in g[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                order.append(v)

    size = [1] * (n + 1)
    for i in range(n - 1, 0, -1):
        v = order[i]
        size[parent[v]] += size[v]

    max_part = [0] * (n + 1)
    for v in range(1, n + 1):
        max_part[v] = n - size[v]
    for i in range(1, n):
        v = order[i]
        p = parent[v]
        if size[v] > max_part[p]:
            max_part[p] = size[v]

    for v in range(1, n + 1):
        if max_part[v] * 2 <= n:
            return v
    return 1
