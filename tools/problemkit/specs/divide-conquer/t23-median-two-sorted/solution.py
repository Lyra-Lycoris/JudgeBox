def solve(n: int, a: list[int], m: int, b: list[int]) -> int:
    def kth(k: int) -> int:
        i = j = 0
        na, nb = len(a), len(b)
        while True:
            if i == na:
                return b[j + k]
            if j == nb:
                return a[i + k]
            if k == 0:
                return a[i] if a[i] < b[j] else b[j]
            step = (k + 1) // 2
            ai = i + min(na - i, step) - 1
            bj = j + min(nb - j, step) - 1
            if a[ai] <= b[bj]:
                k -= ai - i + 1
                i = ai + 1
            else:
                k -= bj - j + 1
                j = bj + 1

    total = n + m
    return kth((total - 1) // 2) + kth(total // 2)
