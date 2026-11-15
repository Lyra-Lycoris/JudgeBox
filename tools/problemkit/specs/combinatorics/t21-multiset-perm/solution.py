MOD = 1000000007


def solve(n: int, a: list[int]) -> int:
    a.sort()
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD
    answer = fact[n]
    i = 0
    while i < n:
        j = i + 1
        while j < n and a[j] == a[i]:
            j += 1
        answer = answer * invfact[j - i] % MOD
        i = j
    return answer
