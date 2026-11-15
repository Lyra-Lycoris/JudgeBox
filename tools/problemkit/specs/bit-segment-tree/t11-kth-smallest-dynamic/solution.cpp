#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long q, const vector<vector<long long>>& ops) {
    vector<long long> values;
    for (const auto& op : ops)
        if (op[0] == 1) values.push_back(op[1]);
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    long long m = (long long)values.size();
    vector<long long> tree(m + 1, 0);
    long long highest = 0;
    while ((1LL << (highest + 1)) <= m) ++highest;
    long long step0 = (m > 0) ? (1LL << highest) : 0;

    vector<long long> answer;
    for (long long j = 0; j < q; ++j) {
        long long t = ops[j][0], x = ops[j][1];
        if (t == 1 || t == 2) {
            long long i = lower_bound(values.begin(), values.end(), x) - values.begin() + 1;
            long long delta = (t == 1) ? 1 : -1;
            for (; i <= m; i += i & -i) tree[i] += delta;
        } else {
            long long k = x, pos = 0, step = step0;
            while (step > 0) {
                long long nxt = pos + step;
                if (nxt <= m && tree[nxt] < k) {
                    pos = nxt;
                    k -= tree[nxt];
                }
                step >>= 1;
            }
            answer.push_back(values[pos]);
        }
    }
    return answer;
}
