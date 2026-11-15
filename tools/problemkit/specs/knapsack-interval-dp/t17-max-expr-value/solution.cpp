#include <bits/stdc++.h>
using namespace std;

long long solve(long long m, const vector<long long>& nums, const vector<string>& ops) {
    const long long NEG = -4000000000000000000LL;
    const long long POS = 4000000000000000000LL;
    vector<vector<long long>> mx(m, vector<long long>(m, NEG));
    vector<vector<long long>> mn(m, vector<long long>(m, POS));
    for (long long i = 0; i < m; ++i) {
        mx[i][i] = nums[i];
        mn[i][i] = nums[i];
    }
    for (long long len = 2; len <= m; ++len) {
        for (long long i = 0; i + len - 1 < m; ++i) {
            long long j = i + len - 1;
            for (long long k = i; k < j; ++k) {
                long long a1 = mx[i][k], a2 = mn[i][k];
                long long b1 = mx[k + 1][j], b2 = mn[k + 1][j];
                long long cand[4];
                int cnt = 0;
                if (ops[k] == "+") {
                    cand[cnt++] = a1 + b1;
                    cand[cnt++] = a2 + b2;
                } else if (ops[k] == "-") {
                    cand[cnt++] = a1 - b2;
                    cand[cnt++] = a2 - b1;
                } else {
                    cand[cnt++] = a1 * b1;
                    cand[cnt++] = a1 * b2;
                    cand[cnt++] = a2 * b1;
                    cand[cnt++] = a2 * b2;
                }
                for (int t = 0; t < cnt; ++t) {
                    if (cand[t] > mx[i][j]) mx[i][j] = cand[t];
                    if (cand[t] < mn[i][j]) mn[i][j] = cand[t];
                }
            }
        }
    }
    return mx[0][m - 1];
}
