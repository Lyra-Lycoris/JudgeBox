def solve(n: int, a: list[int]) -> bool:
    x = 0
    all_one = True
    for v in a:
        x ^= v
        if v != 1:
            all_one = False
    if all_one:
        return n % 2 == 0
    return x != 0
