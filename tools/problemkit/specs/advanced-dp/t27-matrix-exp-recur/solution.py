MOD = 1000000007


def solve(n: int, x: int, y: int, p: int, q: int) -> int:
    if n == 0:
        return x % MOD
    if n == 1:
        return y % MOD
    m00, m01, m10, m11 = p % MOD, q % MOD, 1, 0
    r00, r01, r10, r11 = 1, 0, 0, 1
    e = n - 1
    while e:
        if e & 1:
            r00, r01, r10, r11 = (
                (r00 * m00 + r01 * m10) % MOD,
                (r00 * m01 + r01 * m11) % MOD,
                (r10 * m00 + r11 * m10) % MOD,
                (r10 * m01 + r11 * m11) % MOD,
            )
        m00, m01, m10, m11 = (
            (m00 * m00 + m01 * m10) % MOD,
            (m00 * m01 + m01 * m11) % MOD,
            (m10 * m00 + m11 * m10) % MOD,
            (m10 * m01 + m11 * m11) % MOD,
        )
        e >>= 1
    return (r00 * y + r01 * x) % MOD
