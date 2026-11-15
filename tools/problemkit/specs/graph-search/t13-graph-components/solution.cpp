#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<vector<long long>>& e) {
    vector<int> parent((size_t) n + 1);
    vector<int> rnk((size_t) n + 1, 0);
    for (long long i = 0; i <= n; ++i) parent[i] = (int) i;
    long long count = n;
    for (long long i = 0; i < m; ++i) {
        int a = (int) e[i][0];
        int b = (int) e[i][1];
        while (parent[a] != a) {
            parent[a] = parent[parent[a]];
            a = parent[a];
        }
        while (parent[b] != b) {
            parent[b] = parent[parent[b]];
            b = parent[b];
        }
        if (a == b) continue;
        if (rnk[a] < rnk[b]) swap(a, b);
        parent[b] = a;
        if (rnk[a] == rnk[b]) ++rnk[a];
        --count;
    }
    return count;
}
