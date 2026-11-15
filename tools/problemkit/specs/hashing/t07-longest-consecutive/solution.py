def solve(n: int, a: list[int]) -> int:
    present = set(a)
    best = 0
    for x in a:
        if x - 1 in present:
            continue
        y = x
        while y + 1 in present:
            y += 1
        if y - x + 1 > best:
            best = y - x + 1
    return best
