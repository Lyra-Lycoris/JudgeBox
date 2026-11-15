def solve(n: int, a: list[int]) -> int:
    best = a[0]
    prefix = 0
    min_prefix = 0
    for x in a:
        prefix += x
        candidate = prefix - min_prefix
        if candidate > best:
            best = candidate
        if prefix < min_prefix:
            min_prefix = prefix
    return best
