#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a, long long q,
                        const vector<vector<long long>>& ops) {
    vector<long long> tree(n + 2, 0);
    vector<long long> answer;
    for (long long j = 0; j < q; ++j) {
        long long t = ops[j][0], l = ops[j][1], r = ops[j][2], v = ops[j][3];
        if (t == 1) {
            for (long long i = l; i <= n; i += i & -i) tree[i] += v;
            for (long long i = r + 1; i <= n; i += i & -i) tree[i] -= v;
        } else {
            long long sum = 0;
            for (long long i = l; i > 0; i -= i & -i) sum += tree[i];
            answer.push_back(a[l - 1] + sum);
        }
    }
    return answer;
}
