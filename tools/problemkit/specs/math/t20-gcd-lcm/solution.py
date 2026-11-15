def solve(a: int, b: int) -> list[int]:
    x, y = a, b
    while y:
        x, y = y, x % y
    if x == 0:
        return [0, 0]
    return [x, a // x * b]
