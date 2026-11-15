#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<long long>& blocked) {
    const long long MOD = 1000000007LL;
    int full = 1 << (int)m;
    vector<int> valid;
    valid.reserve((size_t)full);
    for (int s = 0; s < full; ++s) {
        if ((s & (s << 1)) == 0) valid.push_back(s);
    }
    int V = (int)valid.size();
    vector<char> compat((size_t)full * V, 0);
    for (int i = 0; i < V; ++i) {
        int s = valid[i];
        for (int j = 0; j < V; ++j) {
            int t = valid[j];
            if ((s & t) == 0 && ((s << 1) & t) == 0 && ((s >> 1) & t) == 0) {
                compat[(size_t)i * V + j] = 1;
            }
        }
    }
    vector<long long> dp((size_t)full, 0);
    int b0 = (int)blocked[0];
    for (int i = 0; i < V; ++i) {
        int s = valid[i];
        if ((s & b0) == 0) dp[s] = 1;
    }
    for (int row = 1; row < (int)n; ++row) {
        int b = (int)blocked[row];
        vector<long long> ndp((size_t)full, 0);
        for (int i = 0; i < V; ++i) {
            int s = valid[i];
            if (s & b) continue;
            long long total = 0;
            const char* rowPtr = compat.data() + (size_t)i * V;
            for (int j = 0; j < V; ++j) {
                if (rowPtr[j]) total += dp[valid[j]];
            }
            ndp[s] = total % MOD;
        }
        dp.swap(ndp);
    }
    long long ans = 0;
    for (int i = 0; i < V; ++i) ans += dp[valid[i]];
    return ans % MOD;
}
