def solve(n: int, m: int, g: list[list[int]]) -> int:
    total = n * m
    parent = list(range(total))
    size = [1] * total

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    islands = 0
    for r in range(n):
        row = g[r]
        for c in range(m):
            if row[c] != 1:
                continue
            islands += 1
            cur = r * m + c
            if r > 0 and g[r - 1][c] == 1:
                a = find(cur)
                b = find(cur - m)
                if a != b:
                    if size[a] < size[b]:
                        a, b = b, a
                    parent[b] = a
                    size[a] += size[b]
                    islands -= 1
            if c > 0 and row[c - 1] == 1:
                a = find(cur)
                b = find(cur - 1)
                if a != b:
                    if size[a] < size[b]:
                        a, b = b, a
                    parent[b] = a
                    size[a] += size[b]
                    islands -= 1
    return islands
