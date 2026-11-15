def solve(n: int) -> list[int]:
    SHIFT = 40
    a = []
    value = 1
    for i in range(n):
        if i % 2 == 0:
            a.append(value)
        else:
            a.append(value << SHIFT)
            value += 1
    return a
