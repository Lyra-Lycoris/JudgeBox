import heapq


def solve(n: int, m: int, k: int, a: list[int], b: list[int]) -> list[int]:
    heap = [(a[0] + b[0], 0, 0)]
    answer = []
    while len(answer) < k:
        total, i, j = heapq.heappop(heap)
        answer.append(total)
        if i + 1 < n:
            heapq.heappush(heap, (a[i + 1] + b[j], i + 1, j))
        if i == 0 and j + 1 < m:
            heapq.heappush(heap, (a[i] + b[j + 1], i, j + 1))
    return answer
