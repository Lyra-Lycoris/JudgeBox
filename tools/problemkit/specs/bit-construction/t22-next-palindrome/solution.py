def solve(n: int) -> int:
    if n < 10:
        return n
    s = str(n)
    L = len(s)
    half = s[:(L + 1) // 2]

    candidate = int(half + half[:L // 2][::-1])
    if candidate >= n:
        return candidate

    nxt = str(int(half) + 1)
    if len(nxt) > len(half):
        return int('1' + '0' * (L - 1) + '1')
    return int(nxt + nxt[:L // 2][::-1])
