#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a, long long q, const vector<vector<long long>>& ops) {
    vector<long long> cur(a.begin(), a.end());
    vector<long long> bit(n + 1, 0);
    for (long long i = 1; i <= n; ++i) {
        bit[i] += cur[i - 1];
        long long j = i + (i & -i);
        if (j <= n) bit[j] += bit[i];
    }

    long long step0 = 1;
    while ((step0 << 1) <= n) step0 <<= 1;

    vector<long long> answer;
    for (long long k = 0; k < q; ++k) {
        long long t = ops[k][0], x = ops[k][1], v = ops[k][2];
        if (t == 1) {
            long long delta = v - cur[x - 1];
            cur[x - 1] = v;
            for (long long i = x; i <= n; i += i & -i) bit[i] += delta;
        } else {
            long long need = x, pos = 0, step = step0;
            while (step > 0) {
                long long nxt = pos + step;
                if (nxt <= n && bit[nxt] < need) {
                    pos = nxt;
                    need -= bit[nxt];
                }
                step >>= 1;
            }
            answer.push_back(pos + 1);
        }
    }
    return answer;
}
