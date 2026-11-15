import heapq


def solve(n: int, a: list[int]) -> int:
    if n <= 1:
        return 0
    heap = list(a)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        total += x + y
        heapq.heappush(heap, x + y)
    return total
