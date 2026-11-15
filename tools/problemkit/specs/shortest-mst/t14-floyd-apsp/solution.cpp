#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<vector<long long>>& w) {
    const long long INF = (1LL << 62);
    vector<vector<long long>> d(n, vector<long long>(n, INF));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) d[i][j] = (w[i][j] < 0 ? INF : w[i][j]);
        d[i][i] = 0;
    }
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            long long dik = d[i][k];
            if (dik >= INF) continue;
            for (int j = 0; j < n; ++j) {
                long long nd = dik + d[k][j];
                if (nd < d[i][j]) d[i][j] = nd;
            }
        }
    }
    vector<long long> answer;
    answer.reserve((size_t)n * (size_t)n);
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) answer.push_back(d[i][j] >= INF ? -1 : d[i][j]);
    return answer;
}
