def solve(n: int, a: list[int], k: int) -> int:
    rems = [0] * (n + 1)
    cur = 0
    for i, x in enumerate(a):
        cur = (cur + x) % k
        rems[i + 1] = cur
    rems.sort()
    answer = 0
    run = 1
    for i in range(1, n + 1):
        if rems[i] == rems[i - 1]:
            run += 1
        else:
            answer += run * (run - 1) // 2
            run = 1
    answer += run * (run - 1) // 2
    return answer
