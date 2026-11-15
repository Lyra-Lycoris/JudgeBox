def solve(n: int, a: list[int]) -> int:
    best = 0
    mn = a[0]
    for x in a[1:]:
        profit = x - mn
        if profit > best:
            best = profit
        if x < mn:
            mn = x
    return best
