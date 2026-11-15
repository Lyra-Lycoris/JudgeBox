def solve(n: int, m: int, e: list[list[int]]) -> int:
    deg = [0] * (n + 1)
    indeg = [0] * (n + 1)
    has_self = bytearray(n + 1)
    for i in range(m):
        a = e[i][0]
        b = e[i][1]
        deg[a] += 1
        indeg[b] += 1
        if a == b:
            has_self[a] = 1
    start = [0] * (n + 2)
    for v in range(1, n + 1):
        start[v + 1] = start[v] + deg[v]
    rstart = [0] * (n + 2)
    for v in range(1, n + 1):
        rstart[v + 1] = rstart[v] + indeg[v]
    cursor = start[:]
    rcursor = rstart[:]
    adj = [0] * m
    radj = [0] * m
    for i in range(m):
        a = e[i][0]
        b = e[i][1]
        adj[cursor[a]] = b
        cursor[a] += 1
        radj[rcursor[b]] = a
        rcursor[b] += 1

    visited = bytearray(n + 1)
    order = [0] * n
    on = 0
    stack = [0] * n
    it = start[:]
    for s in range(1, n + 1):
        if visited[s]:
            continue
        visited[s] = 1
        sp = 1
        stack[0] = s
        while sp > 0:
            u = stack[sp - 1]
            if it[u] < start[u + 1]:
                v = adj[it[u]]
                it[u] += 1
                if not visited[v]:
                    visited[v] = 1
                    stack[sp] = v
                    sp += 1
            else:
                order[on] = u
                on += 1
                sp -= 1

    comp = [-1] * (n + 1)
    sizes = []
    for idx in range(n - 1, -1, -1):
        s = order[idx]
        if comp[s] != -1:
            continue
        cid = len(sizes)
        comp[s] = cid
        size = 0
        sp = 1
        stack[0] = s
        while sp > 0:
            sp -= 1
            u = stack[sp]
            size += 1
            for k in range(rstart[u], rstart[u + 1]):
                v = radj[k]
                if comp[v] == -1:
                    comp[v] = cid
                    stack[sp] = v
                    sp += 1
        sizes.append(size)

    answer = 0
    for cid in range(len(sizes)):
        if sizes[cid] > 1:
            answer += sizes[cid]
    for v in range(1, n + 1):
        if has_self[v] and sizes[comp[v]] == 1:
            answer += 1
    return answer
