def solve(n: int, m: int, e: list[list[int]]) -> int:
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    count = n
    for i in range(m):
        a = e[i][0]
        b = e[i][1]
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        while parent[b] != b:
            parent[b] = parent[parent[b]]
            b = parent[b]
        if a == b:
            continue
        if rank[a] < rank[b]:
            a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]:
            rank[a] += 1
        count -= 1
    return count
