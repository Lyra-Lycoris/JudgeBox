def solve(n: int, k: int) -> str:
    return "(" * k + ")" * k + "()" * ((n - 2 * k) // 2)
