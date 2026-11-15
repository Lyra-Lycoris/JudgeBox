#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a, long long q, const vector<vector<long long>>& ops) {
    const long long NEG = -(1LL << 62);
    long long blockSize = (long long)sqrt((double)n) + 1;
    long long blocks = (n + blockSize - 1) / blockSize;

    vector<long long> val(a.begin(), a.end());
    vector<long long> lazy(blocks, 0), best(blocks, NEG);
    for (long long i = 0; i < n; ++i) {
        long long b = i / blockSize;
        best[b] = max(best[b], val[i]);
    }

    auto rebuild = [&](long long b) {
        long long lo = b * blockSize;
        long long hi = min(n, lo + blockSize);
        long long m = NEG;
        for (long long i = lo; i < hi; ++i) m = max(m, val[i]);
        best[b] = m;
    };

    vector<long long> answer;
    for (long long k = 0; k < q; ++k) {
        long long t = ops[k][0];
        long long l = ops[k][1] - 1;
        long long r = ops[k][2] - 1;
        long long x = ops[k][3];
        long long bl = l / blockSize, br = r / blockSize;
        if (t == 1) {
            if (bl == br) {
                for (long long i = l; i <= r; ++i) val[i] += x;
                rebuild(bl);
            } else {
                for (long long i = l; i < (bl + 1) * blockSize; ++i) val[i] += x;
                rebuild(bl);
                for (long long i = br * blockSize; i <= r; ++i) val[i] += x;
                rebuild(br);
                for (long long b = bl + 1; b < br; ++b) lazy[b] += x;
            }
        } else {
            long long m = NEG;
            if (bl == br) {
                for (long long i = l; i <= r; ++i) m = max(m, val[i] + lazy[bl]);
            } else {
                for (long long i = l; i < (bl + 1) * blockSize; ++i) m = max(m, val[i] + lazy[bl]);
                for (long long i = br * blockSize; i <= r; ++i) m = max(m, val[i] + lazy[br]);
                for (long long b = bl + 1; b < br; ++b) m = max(m, best[b] + lazy[b]);
            }
            answer.push_back(m);
        }
    }
    return answer;
}
