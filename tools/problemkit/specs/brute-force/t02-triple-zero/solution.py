def solve(n: int, a: list[int]) -> int:
    v = sorted(a)
    total = 0
    for i in range(n - 2):
        l, r = i + 1, n - 1
        while l < r:
            s = v[i] + v[l] + v[r]
            if s == 0:
                if v[l] == v[r]:
                    c = r - l + 1
                    total += c * (c - 1) // 2
                    break
                cl = 1
                while l + cl < r and v[l + cl] == v[l]:
                    cl += 1
                cr = 1
                while r - cr > l and v[r - cr] == v[r]:
                    cr += 1
                total += cl * cr
                l += cl
                r -= cr
            elif s < 0:
                l += 1
            else:
                r -= 1
    return total
