def solve(n: int, k: int, parent: list[int], profit: list[int]) -> int:
    K = k + 1
    children = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        children[parent[i - 1]].append(i)
    NEG = -(1 << 62)

    def dfs(u):
        f = [0, 0 if u == 0 else profit[u - 1]]
        size = 1
        for ch in children[u]:
            fc = dfs(ch)
            sc = len(fc) - 1
            newcap = size + sc
            if newcap > K:
                newcap = K
            g = [NEG] * (newcap + 1)
            g[0] = 0
            for j in range(1, size + 1):
                fj = f[j]
                for t in range(0, sc + 1):
                    if j + t > newcap:
                        break
                    val = fj + fc[t]
                    if val > g[j + t]:
                        g[j + t] = val
            f = g
            size = newcap
        return f

    return dfs(0)[K]
