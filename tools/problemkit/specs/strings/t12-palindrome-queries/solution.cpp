#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, string s, long long q, const vector<vector<long long>>& qs) {
    long long m = (long long)s.size();
    vector<long long> answer((size_t)q, 1);
    const long long bases[2] = {131, 137};
    const long long mods[2] = {1000000007LL, 1000000009LL};
    for (int k = 0; k < 2; ++k) {
        long long base = bases[k], mod = mods[k];
        vector<long long> power((size_t)m + 1, 1);
        for (long long i = 0; i < m; ++i) power[(size_t)(i + 1)] = power[(size_t)i] * base % mod;
        vector<long long> forwardHash((size_t)m + 1, 0), reverseHash((size_t)m + 1, 0);
        for (long long i = 0; i < m; ++i) {
            forwardHash[(size_t)(i + 1)] = (forwardHash[(size_t)i] * base + s[(size_t)i]) % mod;
            reverseHash[(size_t)(i + 1)] = (reverseHash[(size_t)i] * base + s[(size_t)(m - 1 - i)]) % mod;
        }
        for (long long j = 0; j < q; ++j) {
            long long left = qs[(size_t)j][0] - 1;
            long long right = qs[(size_t)j][1];
            long long length = right - left;
            long long direct = (forwardHash[(size_t)right] - forwardHash[(size_t)left] * power[(size_t)length] % mod + mod) % mod;
            long long mirrored = (reverseHash[(size_t)(m - left)] - reverseHash[(size_t)(m - right)] * power[(size_t)length] % mod + mod) % mod;
            if (direct != mirrored) answer[(size_t)j] = 0;
        }
    }
    return answer;
}
