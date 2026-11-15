def solve(s: str) -> int:
    last = [-1] * 256
    best = 0
    left = 0
    for right, ch in enumerate(s):
        code = ord(ch) & 255
        if last[code] >= left:
            left = last[code] + 1
        last[code] = right
        if right - left + 1 > best:
            best = right - left + 1
    return best
