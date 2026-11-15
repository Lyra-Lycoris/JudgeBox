#include <bits/stdc++.h>
using namespace std;

static long long countUpto(long long n, long long zeroMask, long long oneMask) {
    if ((zeroMask & oneMask) != 0) return 0;
    long long both = zeroMask | oneMask;
    long long total = 0;
    bool ok = true;
    for (int i = 59; i >= 0; --i) {
        long long nb = (n >> i) & 1LL;
        long long forcedOne = (oneMask >> i) & 1LL;
        if (forcedOne == 1) {
            if (nb == 0) {
                ok = false;
                break;
            }
        } else if (nb == 1) {
            long long lowMask = (1LL << i) - 1LL;
            int freeBits = i - __builtin_popcountll(both & lowMask);
            total += 1LL << freeBits;
            if (((zeroMask >> i) & 1LL) == 1) {
                ok = false;
                break;
            }
        }
    }
    if (ok) total += 1;
    if (oneMask == 0) total -= 1;
    return total;
}

long long solve(long long n, long long m, const vector<vector<long long>>& cond) {
    vector<long long> groups(m + 1, 0);
    long long total = 1LL << m;
    for (long long mask = 1; mask < total; ++mask) {
        long long zeroMask = 0, oneMask = 0;
        long long size = 0;
        for (long long i = 0; i < m; ++i) {
            if (((mask >> i) & 1LL) == 0) continue;
            ++size;
            long long t = cond[i][0], x = cond[i][1];
            if (t == 1) {
                zeroMask |= x - 1;  // k = 2^p 的倍数 <=> 低 p 位全 0
            } else {
                oneMask |= 1LL << x;
            }
        }
        if ((zeroMask & oneMask) != 0) continue;
        groups[size] += countUpto(n, zeroMask, oneMask);
    }
    long long answer = 0;
    for (long long size = 1; size <= m; ++size) {
        if (size & 1) answer += groups[size];
        else answer -= groups[size];
    }
    return answer;
}
