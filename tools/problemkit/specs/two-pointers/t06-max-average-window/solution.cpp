#include <bits/stdc++.h>
using namespace std;

string solve(long long n, long long k, const vector<long long>& a) {
    long long sum = 0;
    for (long long i = 0; i < k; ++i) sum += a[i];
    long long best = sum;
    for (long long i = k; i < n; ++i) {
        sum += a[i] - a[i - k];
        if (sum > best) best = sum;
    }
    long long g = std::gcd(best < 0 ? -best : best, k);
    long long p = best / g;
    long long q = k / g;
    if (q < 0) {
        p = -p;
        q = -q;
    }
    return to_string(p) + "/" + to_string(q);
}
