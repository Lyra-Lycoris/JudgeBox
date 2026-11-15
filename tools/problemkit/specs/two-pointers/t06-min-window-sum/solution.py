def solve(n: int, s: int, a: list[int]) -> int:
    best = -1
    cur = 0
    left = 0
    for right in range(n):
        cur += a[right]
        while cur >= s:
            length = right - left + 1
            if best < 0 or length < best:
                best = length
            cur -= a[left]
            left += 1
    return 0 if best < 0 else best
