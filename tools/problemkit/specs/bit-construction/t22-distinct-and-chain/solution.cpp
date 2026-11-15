#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n) {
    const long long SHIFT = 40;
    vector<long long> a(n);
    long long value = 1;
    for (long long i = 0; i < n; ++i) {
        if (i % 2 == 0) {
            a[i] = value;
        } else {
            a[i] = value << SHIFT;
            ++value;
        }
    }
    return a;
}
