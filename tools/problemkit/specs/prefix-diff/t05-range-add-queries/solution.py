def solve(n: int, a: list[int], q: int, ops: list[list[int]]) -> list[int]:
    diff = [0] * (n + 1)
    for l, r, v in ops:
        diff[l - 1] += v
        diff[r] -= v
    answer = [0] * n
    cur = 0
    for i in range(n):
        cur += diff[i]
        answer[i] = a[i] + cur
    return answer
