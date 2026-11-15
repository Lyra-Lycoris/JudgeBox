def solve(n: int, e: list[int], q: int, queries: list[int]) -> list[int]:
    g = [[] for _ in range(n + 1)]
    for i in range(0, len(e), 2):
        u = e[i]
        v = e[i + 1]
        g[u].append(v)
        g[v].append(u)

    parent = [1] * (n + 1)
    depth = [0] * (n + 1)
    visited = [False] * (n + 1)
    visited[1] = True
    order = [1]
    for u in order:
        du = depth[u] + 1
        for v in g[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                depth[v] = du
                order.append(v)

    log = max(1, n.bit_length())
    up = [parent]
    for _ in range(1, log):
        prev = up[-1]
        up.append([prev[prev[v]] for v in range(n + 1)])

    answer = []
    for t in range(q):
        u = queries[2 * t]
        v = queries[2 * t + 1]
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        k = 0
        while diff:
            if diff & 1:
                u = up[k][u]
            diff >>= 1
            k += 1
        if u != v:
            for k in range(log - 1, -1, -1):
                pu = up[k][u]
                pv = up[k][v]
                if pu != pv:
                    u = pu
                    v = pv
            u = up[0][u]
        answer.append(u)
    return answer
