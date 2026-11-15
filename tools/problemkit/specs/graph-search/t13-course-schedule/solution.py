def solve(n: int, m: int, e: list[list[int]]) -> bool:
    deg = [0] * (n + 1)
    indeg = [0] * (n + 1)
    start = [0] * (n + 2)
    for i in range(m):
        a = e[i][0]
        b = e[i][1]
        deg[a] += 1
        indeg[b] += 1
    for v in range(1, n + 1):
        start[v + 1] = start[v] + deg[v]
    cursor = start[:]
    adj = [0] * m
    for i in range(m):
        a = e[i][0]
        b = e[i][1]
        adj[cursor[a]] = b
        cursor[a] += 1
    queue = [v for v in range(1, n + 1) if indeg[v] == 0]
    head = 0
    seen = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        seen += 1
        for k in range(start[u], start[u + 1]):
            b = adj[k]
            indeg[b] -= 1
            if indeg[b] == 0:
                queue.append(b)
    return seen == n
