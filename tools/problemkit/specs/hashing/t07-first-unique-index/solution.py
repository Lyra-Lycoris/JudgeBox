def solve(n: int, s: str) -> int:
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - 97] += 1
    for i, ch in enumerate(s):
        if counts[ord(ch) - 97] == 1:
            return i + 1
    return -1
