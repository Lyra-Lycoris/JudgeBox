def solve(n: int, a: list[int]) -> int:
    candidate = a[0]
    balance = 0
    for x in a:
        if balance == 0:
            candidate = x
        balance += 1 if x == candidate else -1
    return candidate
