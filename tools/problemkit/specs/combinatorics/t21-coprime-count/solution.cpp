#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m) {
    vector<long long> primes;
    long long x = m;
    if (x % 2 == 0) {
        primes.push_back(2);
        while (x % 2 == 0) x /= 2;
    }
    for (long long d = 3; d * d <= x; d += 2) {
        if (x % d == 0) {
            primes.push_back(d);
            while (x % d == 0) x /= d;
        }
    }
    if (x > 1) primes.push_back(x);

    long long k = (long long)primes.size();
    long long answer = 0;
    for (long long mask = 0; mask < (1LL << k); ++mask) {
        long long product = 1;
        long long bits = 0;
        for (long long j = 0; j < k; ++j) {
            if ((mask >> j) & 1LL) {
                product *= primes[j];
                bits++;
            }
        }
        long long term = n / product;
        if (bits % 2 == 0) {
            answer += term;
        } else {
            answer -= term;
        }
    }
    return answer;
}
