def solve(n: int, m: int, q: int, e: list[list[int]], queries: list[list[int]]) -> list[int]:
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    head = [-1] * (n + 1)
    nxt = []
    to = []
    wt = []
    used = 0
    for u, v, w in sorted(e, key=lambda x: x[2]):
        ru = find(u)
        rv = find(v)
        if ru != rv:
            parent[ru] = rv
            to.append(v)
            wt.append(w)
            nxt.append(head[u])
            head[u] = len(to) - 1
            to.append(u)
            wt.append(w)
            nxt.append(head[v])
            head[v] = len(to) - 1
            used += 1
            if used == n - 1:
                break

    LOG = 1
    while (1 << LOG) <= n:
        LOG += 1
    up = [[0] * (n + 1) for _ in range(LOG)]
    mx = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)
    up0 = up[0]
    mx0 = mx[0]
    seen = bytearray(n + 1)
    seen[1] = 1
    stack = [1]
    while stack:
        u = stack.pop()
        i = head[u]
        while i != -1:
            v = to[i]
            if not seen[v]:
                seen[v] = 1
                depth[v] = depth[u] + 1
                up0[v] = u
                mx0[v] = wt[i]
                stack.append(v)
            i = nxt[i]
    for k in range(1, LOG):
        upk = up[k]
        mxk = mx[k]
        upk1 = up[k - 1]
        mxk1 = mx[k - 1]
        for v in range(1, n + 1):
            mid = upk1[v]
            upk[v] = upk1[mid]
            a = mxk1[v]
            b = mxk1[mid]
            mxk[v] = a if a > b else b

    answer = []
    for u, v in queries:
        best = 0
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        k = 0
        while diff:
            if diff & 1:
                x = mx[k][u]
                if x > best:
                    best = x
                u = up[k][u]
            diff >>= 1
            k += 1
        if u != v:
            k = LOG - 1
            while k >= 0:
                if up[k][u] != up[k][v]:
                    x = mx[k][u]
                    if x > best:
                        best = x
                    x = mx[k][v]
                    if x > best:
                        best = x
                    u = up[k][u]
                    v = up[k][v]
                k -= 1
            x = mx0[u]
            if x > best:
                best = x
            x = mx0[v]
            if x > best:
                best = x
        answer.append(best)
    return answer
