#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a, long long q,
                        const vector<vector<long long>>& queries) {
    vector<long long> values = a;
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    long long m = (long long)values.size();
    vector<long long> last(m + 1, 0);

    vector<long long> head(n + 1, -1), nxt(q, -1);
    for (long long j = 0; j < q; ++j) {
        long long r = queries[j][1];
        nxt[j] = head[r];
        head[r] = j;
    }

    vector<long long> tree(n + 1, 0);
    vector<long long> answer(q, 0);
    auto add = [&](long long i, long long delta) {
        for (; i <= n; i += i & -i) tree[i] += delta;
    };
    auto prefix = [&](long long i) {
        long long s = 0;
        for (; i > 0; i -= i & -i) s += tree[i];
        return s;
    };

    for (long long r = 1; r <= n; ++r) {
        long long id = lower_bound(values.begin(), values.end(), a[r - 1]) - values.begin() + 1;
        if (last[id] != 0) add(last[id], -1);
        last[id] = r;
        add(r, 1);
        long long upto = prefix(r);
        for (long long j = head[r]; j != -1; j = nxt[j]) {
            answer[j] = upto - prefix(queries[j][0] - 1);
        }
    }
    return answer;
}
