#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long k, const vector<long long>& guesses,
                        const vector<long long>& exact, const vector<long long>& loose) {
    vector<vector<long long>> gd(k, vector<long long>(n, 0));
    for (long long q = 0; q < k; ++q) {
        long long v = guesses[q];
        for (long long i = n - 1; i >= 0; --i) {
            gd[q][i] = v % 10;
            v /= 10;
        }
    }
    long long total = 1;
    for (long long i = 0; i < n; ++i) total *= 10;
    vector<long long> cd(n, 0);
    for (long long code = 0; code < total; ++code) {
        long long t = code;
        for (long long i = n - 1; i >= 0; --i) {
            cd[i] = t % 10;
            t /= 10;
        }
        bool ok = true;
        for (long long q = 0; q < k && ok; ++q) {
            long long a = 0, b = 0;
            long long ca[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
            long long cb[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
            for (long long i = 0; i < n; ++i) {
                if (cd[i] == gd[q][i]) ++a;
                ++ca[cd[i]];
                ++cb[gd[q][i]];
            }
            for (int d = 0; d < 10; ++d) b += min(ca[d], cb[d]);
            b -= a;
            if (a != exact[q] || b != loose[q]) ok = false;
        }
        if (ok) return cd;
    }
    return cd;
}
