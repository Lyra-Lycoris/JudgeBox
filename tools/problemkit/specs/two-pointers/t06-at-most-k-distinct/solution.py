def solve(k: int, s: str) -> int:
    if k <= 0 or not s:
        return 0
    count = [0] * 256
    distinct = 0
    best = 0
    left = 0
    for right, ch in enumerate(s):
        code = ord(ch) & 255
        if count[code] == 0:
            distinct += 1
        count[code] += 1
        while distinct > k:
            left_code = ord(s[left]) & 255
            count[left_code] -= 1
            if count[left_code] == 0:
                distinct -= 1
            left += 1
        if right - left + 1 > best:
            best = right - left + 1
    return best
