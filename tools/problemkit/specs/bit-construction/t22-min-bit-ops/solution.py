def solve(n: int) -> int:
    x = n
    ops = 0
    while x > 0:
        if x % 2 == 0:
            x //= 2
        elif x == 3 or x % 4 == 1:
            x -= 1
        else:
            x += 1
        ops += 1
    return ops
