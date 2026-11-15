def solve(n: int, s: str, q: int, qs: list[list[int]]) -> list[int]:
    m = len(s)
    codes = [ord(ch) for ch in s]
    answer = [1] * q
    for base, mod in ((131, 1000000007), (137, 1000000009)):
        power = [1] * (m + 1)
        for i in range(m):
            power[i + 1] = power[i] * base % mod
        forward = [0] * (m + 1)
        backward = [0] * (m + 1)
        for i in range(m):
            forward[i + 1] = (forward[i] * base + codes[i]) % mod
            backward[i + 1] = (backward[i] * base + codes[m - 1 - i]) % mod
        for j in range(q):
            left = qs[j][0] - 1
            right = qs[j][1]
            length = right - left
            direct = (forward[right] - forward[left] * power[length]) % mod
            mirrored = (backward[m - left] - backward[m - right] * power[length]) % mod
            if direct != mirrored:
                answer[j] = 0
    return answer
