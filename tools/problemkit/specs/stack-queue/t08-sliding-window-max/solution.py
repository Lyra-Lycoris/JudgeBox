from collections import deque


def solve(n: int, k: int, a: list[int]) -> list[int]:
    window = deque()
    answer = []
    for i in range(n):
        while window and a[window[-1]] <= a[i]:
            window.pop()
        window.append(i)
        if window[0] <= i - k:
            window.popleft()
        if i >= k - 1:
            answer.append(a[window[0]])
    return answer
