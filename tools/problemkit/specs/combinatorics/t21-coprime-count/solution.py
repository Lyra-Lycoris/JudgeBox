def solve(n: int, m: int) -> int:
    primes = []
    x = m
    if x % 2 == 0:
        primes.append(2)
        while x % 2 == 0:
            x //= 2
    d = 3
    while d * d <= x:
        if x % d == 0:
            primes.append(d)
            while x % d == 0:
                x //= d
        d += 2
    if x > 1:
        primes.append(x)

    k = len(primes)
    answer = 0
    for mask in range(1 << k):
        product = 1
        bits = 0
        for j in range(k):
            if (mask >> j) & 1:
                product *= primes[j]
                bits += 1
        term = n // product
        if bits % 2 == 0:
            answer += term
        else:
            answer -= term
    return answer
