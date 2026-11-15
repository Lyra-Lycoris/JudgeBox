import heapq


def solve(n: int, a: list[int]) -> int:
    if n <= 1:
        return 0
    heap = list(a)
    heapq.heapify(heap)
    cost = 0
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        cost += x + y
        heapq.heappush(heap, x + y)
    return cost - sum(a)
