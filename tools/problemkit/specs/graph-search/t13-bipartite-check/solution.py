def solve(n: int, m: int, e: list[list[int]]) -> bool:
    deg = [0] * (n + 1)
    for i in range(m):
        deg[e[i][0]] += 1
        deg[e[i][1]] += 1
    start = [0] * (n + 2)
    for v in range(1, n + 1):
        start[v + 1] = start[v] + deg[v]
    cursor = start[:]
    adj = [0] * (2 * m)
    for i in range(m):
        a = e[i][0]
        b = e[i][1]
        adj[cursor[a]] = b
        cursor[a] += 1
        adj[cursor[b]] = a
        cursor[b] += 1
    color = [-1] * (n + 1)
    for s in range(1, n + 1):
        if color[s] != -1:
            continue
        color[s] = 0
        queue = [s]
        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1
            c = color[u] ^ 1
            for k in range(start[u], start[u + 1]):
                v = adj[k]
                if color[v] == -1:
                    color[v] = c
                    queue.append(v)
                elif color[v] == color[u]:
                    return False
    return True
