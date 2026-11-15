import math


def solve(n: int) -> int:
    if n <= 20:
        fact = 1
        for i in range(2, n + 1):
            fact *= i
        return len(str(fact))
    x = float(n)
    value = (x * math.log10(x)
             - x * 0.4342944819032518
             + 0.5 * math.log10(6.283185307179586 * x)
             + 1.0 / (12.0 * x * 2.302585092994046))
    return int(math.floor(value)) + 1
