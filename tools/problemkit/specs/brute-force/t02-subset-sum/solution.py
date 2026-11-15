def solve(target: int, n: int, a: list[int]) -> bool:
    sums = [0]
    for x in a:
        sums += [s + x for s in sums]
    return target in sums
