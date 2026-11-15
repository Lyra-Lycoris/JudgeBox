import heapq


def solve(n: int, k: int, a: list[int]) -> int:
    heap = []
    for x in a:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
