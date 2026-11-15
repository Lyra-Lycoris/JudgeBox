#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long m, const vector<vector<long long>>& g, long long q,
                        const vector<vector<long long>>& queries) {
    vector<vector<long long>> pre(n + 1, vector<long long>(m + 1, 0));
    for (long long i = 1; i <= n; ++i) {
        for (long long j = 1; j <= m; ++j) {
            pre[i][j] = g[i - 1][j - 1] + pre[i - 1][j] + pre[i][j - 1] - pre[i - 1][j - 1];
        }
    }
    vector<long long> answer(q, 0);
    for (long long t = 0; t < q; ++t) {
        long long x1 = queries[t][0], y1 = queries[t][1];
        long long x2 = queries[t][2], y2 = queries[t][3];
        answer[t] = pre[x2][y2] - pre[x1 - 1][y2] - pre[x2][y1 - 1] + pre[x1 - 1][y1 - 1];
    }
    return answer;
}
