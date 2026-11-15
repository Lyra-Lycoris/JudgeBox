#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m) {
    if (n < m) {
        long long t = n;
        n = m;
        m = t;
    }
    int rows = (int)n, cols = (int)m;
    int size = 1 << cols;
    vector<int> valid;
    for (int mask = 0; mask < size; ++mask)
        if ((mask & (mask << 1)) == 0) valid.push_back(mask);
    vector<long long> dp(size, 0), ndp(size, 0);
    for (int mask : valid) dp[mask] = 1;
    for (int r = 1; r < rows; ++r) {
        for (int a : valid) {
            long long sum = 0;
            for (int b : valid) {
                if ((a & b) == 0 && (a & (b << 1)) == 0 && ((a << 1) & b) == 0) sum += dp[b];
            }
            ndp[a] = sum;
        }
        dp.swap(ndp);
    }
    long long total = 0;
    for (int mask : valid) total += dp[mask];
    return total;
}
