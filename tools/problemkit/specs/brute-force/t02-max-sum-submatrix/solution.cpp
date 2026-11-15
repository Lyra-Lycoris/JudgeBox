#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<vector<long long>>& g) {
    long long answer = g[0][0];
    vector<long long> sums(m, 0);
    for (long long top = 0; top < n; ++top) {
        fill(sums.begin(), sums.end(), 0);
        for (long long bottom = top; bottom < n; ++bottom) {
            for (long long c = 0; c < m; ++c) sums[c] += g[bottom][c];
            long long cur = sums[0], best = sums[0];
            for (long long c = 1; c < m; ++c) {
                cur = max(sums[c], cur + sums[c]);
                best = max(best, cur);
            }
            answer = max(answer, best);
        }
    }
    return answer;
}
