#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a) {
    long long limit = 0;
    for (long long x : a) limit = max(limit, x);
    vector<char> sieve((size_t) limit + 1, 1);
    sieve[0] = 0;
    if (limit >= 1) sieve[1] = 0;
    for (long long i = 2; i * i <= limit; ++i) {
        if (sieve[i]) {
            for (long long j = i * i; j <= limit; j += i) sieve[j] = 0;
        }
    }
    vector<long long> primes;
    for (long long i = 0; i <= limit; ++i) {
        if (sieve[i]) primes.push_back(i);
    }
    vector<long long> answer((size_t) n, 0);
    for (long long k = 0; k < n; ++k) {
        answer[k] = upper_bound(primes.begin(), primes.end(), a[k]) - primes.begin();
    }
    return answer;
}
