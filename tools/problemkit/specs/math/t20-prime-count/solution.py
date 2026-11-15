import itertools


def solve(n: int, a: list[int]) -> list[int]:
    limit = max(a) if a else 1
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    p = 2
    while p * p <= limit:
        if sieve[p]:
            start = p * p
            sieve[start::p] = bytearray(len(range(start, limit + 1, p)))
        p += 1
    primes = list(itertools.compress(range(limit + 1), sieve))
    total = len(primes)
    answer = []
    for x in a:
        lo, hi = 0, total
        while lo < hi:
            mid = (lo + hi) // 2
            if primes[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        answer.append(lo)
    return answer
