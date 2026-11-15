def solve(k: int, w: list[str]) -> bool:
    return all(x == w[0] for x in w)
