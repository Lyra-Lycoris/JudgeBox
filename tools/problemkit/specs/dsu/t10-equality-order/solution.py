def solve(n: int, k: int, cons: list[list[int]]) -> bool:
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(k):
        if cons[i][0] == 0:
            a = find(cons[i][1])
            b = find(cons[i][2])
            if a != b:
                if size[a] < size[b]:
                    a, b = b, a
                parent[b] = a
                size[a] += size[b]

    ids = [-1] * (n + 1)
    cnt = 0
    for v in range(1, n + 1):
        r = find(v)
        if ids[r] < 0:
            ids[r] = cnt
            cnt += 1

    adj = [[] for _ in range(cnt)]
    indeg = [0] * cnt
    for i in range(k):
        if cons[i][0] != 1:
            continue
        u = ids[find(cons[i][1])]
        v = ids[find(cons[i][2])]
        if u == v:
            return False
        adj[u].append(v)
        indeg[v] += 1

    stack = [i for i in range(cnt) if indeg[i] == 0]
    seen = 0
    while stack:
        u = stack.pop()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)
    return seen == cnt
