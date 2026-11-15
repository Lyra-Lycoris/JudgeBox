def solve(n: int, a: list[int]) -> list[int]:
    answer = [-1] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and stack[-1] <= a[i]:
            stack.pop()
        if stack:
            answer[i] = stack[-1]
        stack.append(a[i])
    return answer
