def solve(n: int, m: int, e: list[list[int]]) -> int:
    order = sorted((e[i][2], e[i][0], e[i][1]) for i in range(m))
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    used = 0
    for w, u, v in order:
        a = find(u)
        b = find(v)
        if a == b:
            continue
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        total += w
        used += 1
        if used == n - 1:
            break
    if used != n - 1:
        return -1
    return total
