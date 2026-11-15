#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long m, const vector<long long>& r, const vector<long long>& c) {
    const long long SHIFT = 100000;
    const long long BIG = 99999;
    vector<long long> rem(c.begin(), c.end());
    vector<long long> result((size_t)(n * m), 0);
    vector<long long> rowKeys(n);
    for (long long i = 0; i < n; ++i) rowKeys[i] = r[i] * SHIFT + (BIG - i);
    sort(rowKeys.begin(), rowKeys.end());
    vector<long long> colKeys(m);
    for (long long t = n - 1; t >= 0; --t) {
        long long key = rowKeys[t];
        long long i = BIG - key % SHIFT;
        long long need = key / SHIFT;
        if (need == 0) continue;
        for (long long j = 0; j < m; ++j) colKeys[j] = rem[j] * SHIFT + (BIG - j);
        sort(colKeys.begin(), colKeys.end());
        long long base = i * m;
        for (long long p = 0; p < need; ++p) {
            long long ck = colKeys[m - 1 - p];
            long long j = BIG - ck % SHIFT;
            result[(size_t)(base + j)] = 1;
            rem[j] -= 1;
        }
    }
    return result;
}
