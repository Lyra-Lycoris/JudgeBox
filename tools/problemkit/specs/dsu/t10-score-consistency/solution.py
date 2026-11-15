def solve(n: int, k: int, rel: list[list[int]]) -> bool:
    parent = list(range(n + 1))
    size = [1] * (n + 1)
    diff = [0] * (n + 1)  # diff[x] = value[x] - value[parent[x]]

    def find(x: int) -> int:
        root = x
        total = 0
        while parent[root] != root:
            total += diff[root]
            root = parent[root]
        cur = x
        remain = total
        while parent[cur] != cur:
            nxt = parent[cur]
            old = diff[cur]
            parent[cur] = root
            diff[cur] = remain
            remain -= old
            cur = nxt
        return root

    for i in range(k):
        a = rel[i][0]
        b = rel[i][1]
        c = rel[i][2]
        ra = find(a)
        da = diff[a]
        rb = find(b)
        db = diff[b]
        if ra == rb:
            if da - db != c:
                return False
            continue
        if size[ra] < size[rb]:
            parent[ra] = rb
            diff[ra] = -(da - db - c)
            size[rb] += size[ra]
        else:
            parent[rb] = ra
            diff[rb] = da - db - c
            size[ra] += size[rb]
    return True
