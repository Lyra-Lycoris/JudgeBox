#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& p) {
    vector<long long> dp0((size_t)n + 1, 0), dp1((size_t)n + 1, 1);
    for (int i = (int)n; i >= 2; --i) {
        int par = (int)p[i - 2];
        dp0[par] += dp1[i];
        dp1[par] += (dp0[i] < dp1[i] ? dp0[i] : dp1[i]);
    }
    return dp0[1] < dp1[1] ? dp0[1] : dp1[1];
}
