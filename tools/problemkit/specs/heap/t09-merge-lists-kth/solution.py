import heapq


def solve(k: int, m: int, t: int, lists: list[list[int]]) -> int:
    heap = [(lists[r][0], r, 0) for r in range(k)]
    heapq.heapify(heap)
    answer = 0
    for _ in range(t):
        value, r, c = heapq.heappop(heap)
        answer = value
        if c + 1 < m:
            heapq.heappush(heap, (lists[r][c + 1], r, c + 1))
    return answer
