def solve(n: int, l: list[int], r: list[int]) -> int:
    SHIFT = 1000000000
    BASE = 2000000001
    keys = sorted((r[i] + SHIFT) * BASE + (l[i] + SHIFT) for i in range(n))
    answer = 0
    last_end = -(1 << 60)
    for key in keys:
        li = key % BASE - SHIFT
        ri = key // BASE - SHIFT
        if li >= last_end:
            answer += 1
            last_end = ri
    return answer
