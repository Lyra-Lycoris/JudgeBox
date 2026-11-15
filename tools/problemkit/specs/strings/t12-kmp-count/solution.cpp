#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, string s, long long m, string p) {
    if (m <= 0 || (long long)s.size() < m) return 0;
    vector<int> pi((size_t)m, 0);
    for (long long i = 1; i < m; ++i) {
        int k = pi[(size_t)(i - 1)];
        while (k > 0 && p[(size_t)i] != p[(size_t)k]) k = pi[(size_t)(k - 1)];
        if (p[(size_t)i] == p[(size_t)k]) ++k;
        pi[(size_t)i] = k;
    }
    long long count = 0;
    long long k = 0;
    for (char ch : s) {
        while (k > 0 && ch != p[(size_t)k]) k = pi[(size_t)(k - 1)];
        if (ch == p[(size_t)k]) {
            ++k;
            if (k == m) {
                ++count;
                k = pi[(size_t)(k - 1)];
            }
        }
    }
    return count;
}
