def solve(n: int, a: list[int], q: int, ops: list[list[int]]) -> list[int]:
    b1 = [0] * (n + 2)
    b2 = [0] * (n + 2)
    for i in range(1, n + 1):
        v = a[i - 1]
        b1[i] = v
        b2[i] = v * (i - 1)
    for i in range(1, n + 1):
        j = i + (i & -i)
        if j <= n:
            b1[j] += b1[i]
            b2[j] += b2[i]

    answer = []
    for t, l, r, x in ops:
        if t == 1:
            m1 = x * (l - 1)
            m2 = x * r
            i = l
            while i <= n:
                b1[i] += x
                b2[i] += m1
                i += i & -i
            i = r + 1
            while i <= n:
                b1[i] -= x
                b2[i] -= m2
                i += i & -i
        else:
            total = 0
            i = r
            while i > 0:
                total += b1[i] * r - b2[i]
                i -= i & -i
            i = l - 1
            while i > 0:
                total -= b1[i] * (l - 1) - b2[i]
                i -= i & -i
            answer.append(total)
    return answer
