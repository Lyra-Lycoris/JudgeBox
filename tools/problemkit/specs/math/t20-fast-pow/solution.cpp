#include <bits/stdc++.h>
using namespace std;

long long solve(long long a, long long b, long long m) {
    if (m == 1) return 0;
    long long result = 1 % m;
    a %= m;
    while (b > 0) {
        if (b & 1) result = result * a % m;
        a = a * a % m;
        b >>= 1;
    }
    return result;
}
