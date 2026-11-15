#include <bits/stdc++.h>
using namespace std;

static long long kth(const vector<long long>& a, const vector<long long>& b, long long k) {
    int na = (int)a.size(), nb = (int)b.size();
    int i = 0, j = 0;
    while (true) {
        if (i == na) return b[j + (int)k];
        if (j == nb) return a[i + (int)k];
        if (k == 0) return min(a[i], b[j]);
        long long step = (k + 1) / 2;
        int ai = i + (int)min<long long>(na - i, step) - 1;
        int bj = j + (int)min<long long>(nb - j, step) - 1;
        if (a[ai] <= b[bj]) {
            k -= ai - i + 1;
            i = ai + 1;
        } else {
            k -= bj - j + 1;
            j = bj + 1;
        }
    }
}

long long solve(long long n, const vector<long long>& a, long long m, const vector<long long>& b) {
    long long total = n + m;
    return kth(a, b, (total - 1) / 2) + kth(a, b, total / 2);
}
