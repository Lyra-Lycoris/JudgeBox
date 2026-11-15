def solve(n: int, r: int, ch: list[int]) -> list[int]:
    answer = []
    cur = [r]
    forward = True
    while cur:
        answer.extend(cur if forward else reversed(cur))
        nxt = []
        for v in cur:
            base = 2 * (v - 1)
            left = ch[base]
            right = ch[base + 1]
            if left:
                nxt.append(left)
            if right:
                nxt.append(right)
        cur = nxt
        forward = not forward
    return answer
