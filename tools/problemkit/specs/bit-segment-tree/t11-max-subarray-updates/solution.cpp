#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a, long long q,
                        const vector<vector<long long>>& ops) {
    const long long NEG = -(1LL << 61);
    long long size = 1;
    while (size < n) size <<= 1;

    vector<long long> total(size << 1, 0), pref(size << 1, NEG);
    vector<long long> suff(size << 1, NEG), best(size << 1, NEG);
    for (long long i = 0; i < n; ++i) {
        long long k = size + i, v = a[i];
        total[k] = v;
        pref[k] = v;
        suff[k] = v;
        best[k] = v;
    }
    for (long long k = size - 1; k > 0; --k) {
        long long lc = k << 1, rc = lc | 1;
        total[k] = total[lc] + total[rc];
        pref[k] = max(pref[lc], total[lc] + pref[rc]);
        suff[k] = max(suff[rc], total[rc] + suff[lc]);
        best[k] = max(max(best[lc], best[rc]), suff[lc] + pref[rc]);
    }

    vector<long long> answer;
    for (long long j = 0; j < q; ++j) {
        long long t = ops[j][0], x = ops[j][1], y = ops[j][2];
        if (t == 1) {
            long long k = size + x - 1;
            total[k] = pref[k] = suff[k] = best[k] = y;
            for (k >>= 1; k > 0; k >>= 1) {
                long long lc = k << 1, rc = lc | 1;
                total[k] = total[lc] + total[rc];
                pref[k] = max(pref[lc], total[lc] + pref[rc]);
                suff[k] = max(suff[rc], total[rc] + suff[lc]);
                best[k] = max(max(best[lc], best[rc]), suff[lc] + pref[rc]);
            }
        } else {
            long long l = size + x - 1, r = size + y;
            long long ls = 0, lp = NEG, lsf = NEG, lb = NEG;
            long long rs = 0, rp = NEG, rsf = NEG, rb = NEG;
            while (l < r) {
                if (l & 1) {
                    long long ns = ls + total[l];
                    long long np = max(lp, ls + pref[l]);
                    long long nsf = max(suff[l], total[l] + lsf);
                    long long nb = max(max(lb, best[l]), lsf + pref[l]);
                    ls = ns;
                    lp = np;
                    lsf = nsf;
                    lb = nb;
                    ++l;
                }
                if (r & 1) {
                    --r;
                    long long ns = total[r] + rs;
                    long long np = max(pref[r], total[r] + rp);
                    long long nsf = max(rsf, rs + suff[r]);
                    long long nb = max(max(best[r], rb), suff[r] + rp);
                    rs = ns;
                    rp = np;
                    rsf = nsf;
                    rb = nb;
                }
                l >>= 1;
                r >>= 1;
            }
            answer.push_back(max(max(lb, rb), lsf + rp));
        }
    }
    return answer;
}
