def solve(n: int, w: list[int], e: list[int], q: int, queries: list[int]) -> list[int]:
    g = [[] for _ in range(n + 1)]
    for i in range(0, len(e), 2):
        u = e[i]
        v = e[i + 1]
        g[u].append(v)
        g[v].append(u)

    parent = [1] * (n + 1)
    depth = [0] * (n + 1)
    pre = [0] * (n + 1)
    visited = [False] * (n + 1)
    visited[1] = True
    pre[1] = w[0]
    order = [1]
    for u in order:
        du = depth[u] + 1
        pu = pre[u]
        for v in g[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                depth[v] = du
                pre[v] = pu + w[v - 1]
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
        a = u
        b = v
        if depth[a] < depth[b]:
            a, b = b, a
        diff = depth[a] - depth[b]
        k = 0
        while diff:
            if diff & 1:
                a = up[k][a]
            diff >>= 1
            k += 1
        if a != b:
            for k in range(log - 1, -1, -1):
                pa = up[k][a]
                pb = up[k][b]
                if pa != pb:
                    a = pa
                    b = pb
            a = up[0][a]
        answer.append(pre[u] + pre[v] - 2 * pre[a] + w[a - 1])
    return answer
