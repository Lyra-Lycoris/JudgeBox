from collections import deque


def solve(start: str, target: str, n: int, dead: list[str]) -> int:
    blocked = [False] * 10000
    for code in dead:
        blocked[int(code)] = True
    begin = int(start)
    goal = int(target)
    if blocked[begin] or blocked[goal]:
        return -1
    if begin == goal:
        return 0
    dist = [-1] * 10000
    dist[begin] = 0
    queue = deque([begin])
    power = (1, 10, 100, 1000)
    while queue:
        cur = queue.popleft()
        step = dist[cur] + 1
        for p in power:
            digit = (cur // p) % 10
            for nd in ((digit + 1) % 10, (digit + 9) % 10):
                nxt = cur + (nd - digit) * p
                if dist[nxt] == -1 and not blocked[nxt]:
                    dist[nxt] = step
                    if nxt == goal:
                        return step
                    queue.append(nxt)
    return -1
