#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& w, const vector<long long>& p) {
    vector<long long> dp0((size_t)n + 1, 0), dp1((size_t)n + 1, 0);
    for (int i = 1; i <= (int)n; ++i) dp1[i] = w[i - 1];
    for (int i = (int)n; i >= 2; --i) {
        int par = (int)p[i - 2];
        long long a = dp0[i], b = dp1[i];
        dp0[par] += (a > b ? a : b);
        dp1[par] += a;
    }
    return dp0[1] > dp1[1] ? dp0[1] : dp1[1];
}
