#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a, long long q,
                        const vector<vector<long long>>& ops) {
    vector<long long> tree(n + 1, 0);
    for (long long i = 1; i <= n; ++i) {
        tree[i] += a[i - 1];
        long long up = i + (i & -i);
        if (up <= n) tree[up] += tree[i];
    }
    vector<long long> answer;
    for (long long j = 0; j < q; ++j) {
        if (ops[j][0] == 1) {
            long long i = ops[j][1], v = ops[j][2];
            while (i <= n) {
                tree[i] += v;
                i += i & -i;
            }
        } else {
            long long sum = 0;
            for (long long i = ops[j][2]; i > 0; i -= i & -i) sum += tree[i];
            for (long long i = ops[j][1] - 1; i > 0; i -= i & -i) sum -= tree[i];
            answer.push_back(sum);
        }
    }
    return answer;
}
