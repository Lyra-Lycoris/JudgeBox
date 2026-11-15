def solve(a: int, b: int, m: int) -> int:
    def power(base: int, exp: int) -> int:
        if exp == 0:
            return 1 % m
        half = power(base, exp // 2)
        result = half * half % m
        if exp & 1:
            result = result * (base % m) % m
        return result

    return power(a % m, b)
