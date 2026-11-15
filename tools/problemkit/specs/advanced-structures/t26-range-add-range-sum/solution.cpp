#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a, long long q, const vector<vector<long long>>& ops) {
    vector<long long> b1(n + 2, 0), b2(n + 2, 0);
    for (long long i = 1; i <= n; ++i) {
        b1[i] = a[i - 1];
        b2[i] = a[i - 1] * (i - 1);
    }
    for (long long i = 1; i <= n; ++i) {
        long long j = i + (i & -i);
        if (j <= n) {
            b1[j] += b1[i];
            b2[j] += b2[i];
        }
    }

    vector<long long> answer;
    for (long long k = 0; k < q; ++k) {
        long long t = ops[k][0], l = ops[k][1], r = ops[k][2], x = ops[k][3];
        if (t == 1) {
            for (long long i = l; i <= n; i += i & -i) {
                b1[i] += x;
                b2[i] += x * (l - 1);
            }
            for (long long i = r + 1; i <= n; i += i & -i) {
                b1[i] -= x;
                b2[i] -= x * r;
            }
        } else {
            long long total = 0;
            for (long long i = r; i > 0; i -= i & -i) total += b1[i] * r - b2[i];
            for (long long i = l - 1; i > 0; i -= i & -i) total -= b1[i] * (l - 1) - b2[i];
            answer.push_back(total);
        }
    }
    return answer;
}
