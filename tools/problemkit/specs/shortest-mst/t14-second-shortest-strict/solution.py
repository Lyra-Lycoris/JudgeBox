import heapq


def solve(n: int, m: int, e: list[list[int]]) -> int:
    graph = [[] for _ in range(n + 1)]
    for u, v, w in e:
        graph[u].append((v, w))
        graph[v].append((u, w))
    INF = 10 ** 30
    d1 = [INF] * (n + 1)
    d2 = [INF] * (n + 1)
    d1[1] = 0
    heap = [(0, 1)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > d2[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < d1[v]:
                d2[v] = d1[v]
                d1[v] = nd
                heapq.heappush(heap, (nd, v))
            elif nd > d1[v] and nd < d2[v]:
                d2[v] = nd
                heapq.heappush(heap, (nd, v))
    return -1 if d2[n] >= INF else d2[n]
