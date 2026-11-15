#include <bits/stdc++.h>
using namespace std;

long long solve(string s) {
    long long n = (long long) s.size();
    if (n <= 1) return 0;
    vector<long long> dp(n + 1, n + 1);
    dp[0] = 0;
    for (long long c = 0; c < n; ++c) {
        for (long long l = c, r = c; l >= 0 && r < n && s[l] == s[r]; --l, ++r) {
            if (dp[l] + 1 < dp[r + 1]) dp[r + 1] = dp[l] + 1;
        }
        for (long long l = c, r = c + 1; l >= 0 && r < n && s[l] == s[r]; --l, ++r) {
            if (dp[l] + 1 < dp[r + 1]) dp[r + 1] = dp[l] + 1;
        }
    }
    return dp[n] - 1;
}
