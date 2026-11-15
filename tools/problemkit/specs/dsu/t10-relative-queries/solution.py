def solve(n: int, k: int, rel: list[list[int]], q: int, qs: list[list[int]]) -> int:
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(k):
        a = find(rel[i][0])
        b = find(rel[i][1])
        if a == b:
            continue
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]

    answer = 0
    for i in range(q):
        if find(qs[i][0]) == find(qs[i][1]):
            answer += 1
    return answer
