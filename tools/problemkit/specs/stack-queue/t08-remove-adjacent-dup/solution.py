def solve(k: int, s: str) -> str:
    chars = []
    counts = []
    for ch in s:
        if chars and chars[-1] == ch:
            counts[-1] += 1
            if counts[-1] == k:
                chars.pop()
                counts.pop()
        else:
            chars.append(ch)
            counts.append(1)
    return "".join(ch * count for ch, count in zip(chars, counts))
