import heapq


def solve(n: int, m: int, s: list[int], d: list[int]) -> int:
    order = sorted(range(m), key=lambda i: (s[i], i))
    free = list(range(n))
    heapq.heapify(free)
    busy = []
    used = [0] * n
    for idx in order:
        start = s[idx]
        while busy and busy[0][0] <= start:
            finish, room = heapq.heappop(busy)
            heapq.heappush(free, room)
        if free:
            room = heapq.heappop(free)
            heapq.heappush(busy, (start + d[idx], room))
        else:
            finish, room = heapq.heappop(busy)
            heapq.heappush(busy, (finish + d[idx], room))
        used[room] += 1
    best = 0
    for i in range(1, n):
        if used[i] > used[best]:
            best = i
    return best
