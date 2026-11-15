def solve(n: int, a: list[int]) -> int:
    not_take = 0
    take = a[0]
    for x in a[1:]:
        if not_take > take:
            best = not_take
        else:
            best = take
        not_take, take = best, not_take + x
    return take if take > not_take else not_take
