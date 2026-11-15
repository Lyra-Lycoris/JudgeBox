def solve(m: int, op: list[int], val: list[int]) -> list[int]:
    stack = []
    minimum = []
    answer = []
    for i in range(m):
        if op[i] == 1:
            v = val[i]
            stack.append(v)
            minimum.append(v if not minimum else min(minimum[-1], v))
        elif op[i] == 2:
            stack.pop()
            minimum.pop()
        else:
            answer.append(minimum[-1])
    return answer
