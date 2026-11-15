#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a, long long q,
                        const vector<vector<long long>>& ops) {
    vector<long long> diff(n + 1, 0);
    for (long long j = 0; j < q; ++j) {
        long long l = ops[j][0], r = ops[j][1], v = ops[j][2];
        diff[l - 1] += v;
        diff[r] -= v;
    }
    vector<long long> answer(n, 0);
    long long cur = 0;
    for (long long i = 0; i < n; ++i) {
        cur += diff[i];
        answer[i] = a[i] + cur;
    }
    return answer;
}
