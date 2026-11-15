def solve(n: int, q: int, segs: list[list[int]]) -> list[int]:
    diff = [0] * (n + 1)
    for l, r in segs:
        diff[l - 1] += 1
        diff[r] -= 1
    cur = 0
    best = -1
    best_pos = 1
    for i in range(n):
        cur += diff[i]
        if cur > best:
            best = cur
            best_pos = i + 1
    return [best, best_pos]
