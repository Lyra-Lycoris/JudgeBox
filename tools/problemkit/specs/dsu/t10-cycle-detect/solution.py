def solve(n: int, m: int, e: list[list[int]]) -> bool:
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(m):
        a = find(e[i][0])
        b = find(e[i][1])
        if a == b:
            return True
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
    return False
