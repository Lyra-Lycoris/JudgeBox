#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long m, const vector<vector<long long>>& a, long long q, const vector<vector<long long>>& ops) {
    int r = (int)n, c = (int)m;
    vector<vector<long long>> pre(r + 1, vector<long long>(c + 1, 0));
    for (int i = 1; i <= r; ++i) {
        long long rowSum = 0;
        for (int j = 1; j <= c; ++j) {
            rowSum += a[i - 1][j - 1];
            pre[i][j] = pre[i - 1][j] + rowSum;
        }
    }

    vector<vector<long long>> bit(r + 1, vector<long long>(c + 1, 0));
    for (int i = 1; i <= r; ++i) {
        int li = i - (i & -i);
        for (int j = 1; j <= c; ++j) {
            int lj = j - (j & -j);
            bit[i][j] = pre[i][j] - pre[li][j] - pre[i][lj] + pre[li][lj];
        }
    }

    auto prefixSum = [&](int x, int y) {
        long long s = 0;
        for (int i = x; i > 0; i -= i & -i)
            for (int j = y; j > 0; j -= j & -j) s += bit[i][j];
        return s;
    };

    vector<long long> answer;
    for (long long k = 0; k < q; ++k) {
        long long t = ops[k][0];
        int x = (int)ops[k][1], y = (int)ops[k][2];
        if (t == 1) {
            long long v = ops[k][3];
            for (int i = x; i <= r; i += i & -i)
                for (int j = y; j <= c; j += j & -j) bit[i][j] += v;
        } else {
            int x2 = (int)ops[k][3], y2 = (int)ops[k][4];
            long long total = prefixSum(x2, y2) - prefixSum(x - 1, y2)
                            - prefixSum(x2, y - 1) + prefixSum(x - 1, y - 1);
            answer.push_back(total);
        }
    }
    return answer;
}
