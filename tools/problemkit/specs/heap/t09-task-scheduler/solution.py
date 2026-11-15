import heapq


def solve(n: int, c: int, tasks: list[int]) -> int:
    count = {}
    for x in tasks:
        count[x] = count.get(x, 0) + 1
    heap = [-v for v in count.values()]
    heapq.heapify(heap)
    time = 0
    while heap:
        slot = min(c + 1, len(heap))
        rest = []
        for _ in range(slot):
            top = -heapq.heappop(heap)
            if top > 1:
                rest.append(top - 1)
        time += c + 1
        for x in rest:
            heapq.heappush(heap, -x)
        if not heap:
            time -= c + 1 - slot
    return time
