def solve(n: int, m: int, e: list[list[int]]) -> list[int]:
    dsu = list(range(n + 1))
    dsu_size = [1] * (n + 1)

    def find(x: int) -> int:
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    for i in range(m):
        a = find(e[i][0])
        b = find(e[i][1])
        if a == b:
            continue
        if dsu_size[a] < dsu_size[b]:
            a, b = b, a
        dsu[b] = a
        dsu_size[a] += dsu_size[b]

    # 每个连通块必须满足 边数 <= 点数，即只允许「树」或「基环树」
    edge_count = [0] * (n + 1)
    for i in range(m):
        edge_count[find(e[i][0])] += 1
    for v in range(1, n + 1):
        if dsu[v] == v and edge_count[v] > dsu_size[v]:
            return [-1]

    # 邻接表（链式前向星）
    head = [-1] * (n + 1)
    to = [0] * (2 * m)
    nxt = [0] * (2 * m)
    eid = [0] * (2 * m)
    cnt = 0
    for i in range(m):
        a = e[i][0]
        b = e[i][1]
        to[cnt] = b
        eid[cnt] = i
        nxt[cnt] = head[a]
        head[a] = cnt
        cnt += 1
        to[cnt] = a
        eid[cnt] = i
        nxt[cnt] = head[b]
        head[b] = cnt
        cnt += 1

    visited = bytearray(n + 1)
    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    pedge = [-1] * (n + 1)
    cur = head[:]
    ans = [0] * (2 * m)
    stack = []
    for s in range(1, n + 1):
        if visited[s]:
            continue
        visited[s] = 1
        parent[s] = 0
        depth[s] = 0
        stack.append(s)
        while stack:
            u = stack[-1]
            j = cur[u]
            if j == -1:
                stack.pop()
                continue
            cur[u] = nxt[j]
            v = to[j]
            k = eid[j]
            if k == pedge[u]:
                continue
            if not visited[v]:
                visited[v] = 1
                parent[v] = u
                pedge[v] = k
                depth[v] = depth[u] + 1
                ans[2 * k] = u
                ans[2 * k + 1] = v
                stack.append(v)
            elif depth[v] < depth[u]:
                # 唯一的返祖边：深的端点指向浅的端点，与环上的树边组成有向环
                ans[2 * k] = u
                ans[2 * k + 1] = v
                # 环顶 v 到 DFS 根之间那条「柄」上的树边必须反着走，
                # 否则 v 会同时收到柄和返祖边两条入边。
                c = v
                while parent[c] != 0:
                    k2 = pedge[c]
                    ans[2 * k2] = c
                    ans[2 * k2 + 1] = parent[c]
                    c = parent[c]
    return ans
