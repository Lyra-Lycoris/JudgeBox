def solve(n: int, a: list[int], target: int) -> bool:
    seen = set()
    for x in a:
        if target - x in seen:
            return True
        seen.add(x)
    return False
