def _prefix_hashes(text: str, base: int, mod: int) -> list[int]:
    prefix = [0] * (len(text) + 1)
    value = 0
    for i, ch in enumerate(text):
        value = (value * base + ord(ch)) % mod
        prefix[i + 1] = value
    return prefix


def solve(n: int, s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    m = len(s)
    doubled = s + s
    for base, mod in ((131, 1000000007), (137, 1000000009)):
        power = pow(base, m, mod)
        target = 0
        for ch in t:
            target = (target * base + ord(ch)) % mod
        prefix = _prefix_hashes(doubled, base, mod)
        matched = False
        for i in range(m):
            if (prefix[i + m] - prefix[i] * power) % mod == target:
                matched = True
                break
        if not matched:
            return False
    return True
