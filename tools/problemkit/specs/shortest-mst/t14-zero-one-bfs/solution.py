from collections import deque


def solve(n: int, m: int, g: list[list[int]]) -> int:
    total = n * m
    cell = [0] * total
    for i in range(n):
        row = g[i]
        base = i * m
        for j in range(m):
            cell[base + j] = row[j]
    INF = 10 ** 9
    dist = [INF] * total
    dist[0] = 0
    dq = deque([0])
    while dq:
        u = dq.popleft()
        du = dist[u]
        r = u // m
        c = u - r * m
        nd = du + 0
        if r > 0:
            v = u - m
            nd = du + cell[v]
            if nd < dist[v]:
                dist[v] = nd
                if cell[v] == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
        if r + 1 < n:
            v = u + m
            nd = du + cell[v]
            if nd < dist[v]:
                dist[v] = nd
                if cell[v] == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
        if c > 0:
            v = u - 1
            nd = du + cell[v]
            if nd < dist[v]:
                dist[v] = nd
                if cell[v] == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
        if c + 1 < m:
            v = u + 1
            nd = du + cell[v]
            if nd < dist[v]:
                dist[v] = nd
                if cell[v] == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist[total - 1]
