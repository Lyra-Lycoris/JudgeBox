def solve(n: int, ids: list[int], chinese: list[int], math: list[int], english: list[int]) -> list[int]:
    order = sorted(range(n), key=lambda i: (-(chinese[i] + math[i] + english[i]), -chinese[i], ids[i]))
    return [ids[i] for i in order]
