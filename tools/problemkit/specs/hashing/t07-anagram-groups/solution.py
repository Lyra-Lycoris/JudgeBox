def solve(n: int, words: list[str]) -> int:
    return len({''.join(sorted(word)) for word in words})
