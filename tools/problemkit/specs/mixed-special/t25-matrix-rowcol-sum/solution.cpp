#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long m, const vector<long long>& r, const vector<long long>& c) {
    vector<long long> row(r.begin(), r.end());
    vector<long long> col(c.begin(), c.end());
    vector<long long> a;
    a.reserve((size_t)(n * m));
    for (long long i = 0; i < n; ++i) {
        for (long long j = 0; j < m; ++j) {
            long long x = min(row[i], col[j]);
            a.push_back(x);
            row[i] -= x;
            col[j] -= x;
        }
    }
    return a;
}
