import heapq


def solve(n: int, k: int, arrive: list[int], serve: list[int]) -> int:
    free_at = [0] * k
    heapq.heapify(free_at)
    total = 0
    for i in range(n):
        free = heapq.heappop(free_at)
        start = free if free > arrive[i] else arrive[i]
        total += start - arrive[i]
        heapq.heappush(free_at, start + serve[i])
    return total
