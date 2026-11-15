import heapq


def solve(n: int, m: int, s: int, e: list[list[int]]) -> list[int]:
    graph = [[] for _ in range(n + 1)]
    for u, v, w in e:
        graph[u].append((v, w))
    INF = 10 ** 30
    dist = [INF] * (n + 1)
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return [-1 if dist[i] >= INF else dist[i] for i in range(1, n + 1)]
