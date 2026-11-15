#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<vector<long long>>& p) {
    const long long INF = (1LL << 62);
    vector<long long> best(n, INF);
    vector<char> used(n, 0);
    best[0] = 0;
    long long total = 0;
    for (long long round = 0; round < n; ++round) {
        int u = -1;
        long long bd = INF;
        for (int i = 0; i < n; ++i) {
            if (!used[i] && best[i] < bd) {
                bd = best[i];
                u = i;
            }
        }
        used[u] = 1;
        total += bd;
        long long xu = p[u][0], yu = p[u][1];
        for (int i = 0; i < n; ++i) {
            if (used[i]) continue;
            long long d = llabs(p[i][0] - xu) + llabs(p[i][1] - yu);
            if (d < best[i]) best[i] = d;
        }
    }
    return total;
}
