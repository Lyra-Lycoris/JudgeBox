def solve(n: int, a: list[int]) -> int:
    best = 0
    zeros = 0
    left = 0
    for right in range(n):
        if a[right] == 0:
            zeros += 1
        while zeros > 1:
            if a[left] == 0:
                zeros -= 1
            left += 1
        if right - left + 1 > best:
            best = right - left + 1
    return best - 1 if best > 0 else 0
