#include <bits/stdc++.h>
using namespace std;

long long solve(long long n) {
    long long result = n;
    long long x = n;
    for (long long p = 2; p * p <= x; ++p) {
        if (x % p == 0) {
            while (x % p == 0) x /= p;
            result -= result / p;
        }
    }
    if (x > 1) result -= result / x;
    return result;
}
