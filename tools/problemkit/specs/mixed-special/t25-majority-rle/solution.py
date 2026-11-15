def solve(k: int, v: list[int], c: list[int]) -> int:
    cand = 0
    balance = 0
    for i in range(k):
        value = v[i]
        cnt = c[i]
        if balance == 0:
            cand = value
            balance = cnt
        elif value == cand:
            balance += cnt
        elif cnt < balance:
            balance -= cnt
        else:
            cand = value
            balance = cnt - balance
    return cand
