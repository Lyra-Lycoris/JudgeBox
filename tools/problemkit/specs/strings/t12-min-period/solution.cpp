#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, string s) {
    long long m = (long long)s.size();
    if (m <= 0) return 0;
    vector<long long> pi((size_t)m, 0);
    for (long long i = 1; i < m; ++i) {
        long long k = pi[(size_t)(i - 1)];
        while (k > 0 && s[(size_t)i] != s[(size_t)k]) k = pi[(size_t)(k - 1)];
        if (s[(size_t)i] == s[(size_t)k]) ++k;
        pi[(size_t)i] = k;
    }
    long long d = m - pi[(size_t)(m - 1)];
    return (m % d == 0) ? d : m;
}
