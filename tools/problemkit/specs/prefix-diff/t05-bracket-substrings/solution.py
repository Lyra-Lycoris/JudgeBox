def solve(s: str) -> int:
    n = len(s)
    counts = [0] * (2 * n + 1)
    stack = [0]
    counts[n] = 1
    prefix = 0
    answer = 0
    for ch in s:
        prefix += 1 if ch == "(" else -1
        while stack and stack[-1] > prefix:
            counts[stack.pop() + n] = 0
        answer += counts[prefix + n]
        counts[prefix + n] += 1
        if not stack or stack[-1] < prefix:
            stack.append(prefix)
    return answer
