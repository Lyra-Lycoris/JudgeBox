def solve(n: int, k: int, guesses: list[int], exact: list[int], loose: list[int]) -> list[int]:
    gd = []
    for g in guesses:
        d = [0] * n
        for i in range(n - 1, -1, -1):
            d[i] = g % 10
            g //= 10
        gd.append(d)

    for code in range(10 ** n):
        t = code
        cd = [0] * n
        for i in range(n - 1, -1, -1):
            cd[i] = t % 10
            t //= 10
        ok = True
        for q in range(k):
            g = gd[q]
            a = 0
            ca = [0] * 10
            cb = [0] * 10
            for i in range(n):
                if cd[i] == g[i]:
                    a += 1
                ca[cd[i]] += 1
                cb[g[i]] += 1
            b = sum(ca[d] if ca[d] < cb[d] else cb[d] for d in range(10)) - a
            if a != exact[q] or b != loose[q]:
                ok = False
                break
        if ok:
            return cd
    return [0] * n
