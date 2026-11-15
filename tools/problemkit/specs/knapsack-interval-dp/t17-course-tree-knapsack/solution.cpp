#include <bits/stdc++.h>
using namespace std;

static vector<long long> dfsCourse(long long u, const vector<vector<long long>>& children,
                                   const vector<long long>& profit, long long limit) {
    vector<long long> f(2);
    f[0] = 0;
    f[1] = (u == 0) ? 0 : profit[u - 1];
    long long size = 1;
    for (long long ch : children[u]) {
        vector<long long> fc = dfsCourse(ch, children, profit, limit);
        long long sc = (long long) fc.size() - 1;
        long long newcap = min(size + sc, limit);
        vector<long long> g(newcap + 1, LLONG_MIN / 4);
        g[0] = 0;
        for (long long j = 1; j <= size; ++j) {
            for (long long t = 0; t <= sc && j + t <= newcap; ++t) {
                long long val = f[j] + fc[t];
                if (val > g[j + t]) g[j + t] = val;
            }
        }
        f.swap(g);
        size = newcap;
    }
    return f;
}

long long solve(long long n, long long k, const vector<long long>& parent, const vector<long long>& profit) {
    vector<vector<long long>> children(n + 1);
    for (long long i = 1; i <= n; ++i) children[parent[i - 1]].push_back(i);
    long long limit = k + 1;
    vector<long long> f = dfsCourse(0, children, profit, limit);
    return f[limit];
}
