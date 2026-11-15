def solve(k: int, words: list[str]) -> int:
    limit = min(len(w) for w in words)
    base = words[0]
    i = 0
    while i < limit:
        ch = base[i]
        for w in words:
            if w[i] != ch:
                return i
        i += 1
    return i
