def solve(n: int, a: list[int], q: int, ops: list[list[int]]) -> list[int]:
    cur = list(a)
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] += cur[i - 1]
        j = i + (i & -i)
        if j <= n:
            bit[j] += bit[i]

    step0 = 1
    while (step0 << 1) <= n:
        step0 <<= 1

    answer = []
    for t, x, v in ops:
        if t == 1:
            delta = v - cur[x - 1]
            cur[x - 1] = v
            i = x
            while i <= n:
                bit[i] += delta
                i += i & -i
        else:
            need = x
            pos = 0
            step = step0
            while step:
                nxt = pos + step
                if nxt <= n and bit[nxt] < need:
                    pos = nxt
                    need -= bit[nxt]
                step >>= 1
            answer.append(pos + 1)
    return answer
