MOD = 1000000007


def solve(n: int) -> int:
    def fib_pair(index: int) -> tuple[int, int]:
        if index == 0:
            return 0, 1
        a, b = fib_pair(index >> 1)
        c = a * ((2 * b - a) % MOD) % MOD
        d = (a * a + b * b) % MOD
        if index & 1:
            return d, (c + d) % MOD
        return c, d

    return fib_pair(n)[0]
