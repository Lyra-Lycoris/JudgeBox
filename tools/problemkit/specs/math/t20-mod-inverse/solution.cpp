#include <bits/stdc++.h>
using namespace std;

long long solve(long long a, long long m) {
    long long old_r = a, r = m;
    long long old_s = 1, s = 0;
    while (r != 0) {
        long long q = old_r / r;
        long long next_r = old_r - q * r;
        old_r = r;
        r = next_r;
        long long next_s = old_s - q * s;
        old_s = s;
        s = next_s;
    }
    if (old_r != 1) return -1;
    long long inv = old_s % m;
    if (inv < 0) inv += m;
    return inv;
}
