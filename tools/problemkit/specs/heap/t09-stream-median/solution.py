import heapq


def solve(n: int, a: list[int]) -> list[int]:
    low = []
    high = []
    answer = []
    for i, x in enumerate(a):
        if not low or x <= -low[0]:
            heapq.heappush(low, -x)
        else:
            heapq.heappush(high, x)
        target = (i + 2) // 2
        while len(low) > target:
            heapq.heappush(high, -heapq.heappop(low))
        while len(low) < target:
            heapq.heappush(low, -heapq.heappop(high))
        answer.append(-low[0])
    return answer
