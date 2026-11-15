#include <bits/stdc++.h>
using namespace std;

struct Node {
    long long sum = 0;
    long long pre = LLONG_MIN / 4;
    long long suf = LLONG_MIN / 4;
    long long best = LLONG_MIN / 4;
};

static Node mergeNode(const Node& L, const Node& R) {
    Node res;
    res.sum = L.sum + R.sum;
    res.pre = max(L.pre, L.sum + R.pre);
    res.suf = max(R.suf, R.sum + L.suf);
    res.best = max(max(L.best, R.best), L.suf + R.pre);
    return res;
}

vector<long long> solve(long long n, const vector<long long>& a, long long q, const vector<vector<long long>>& ops) {
    const long long NEG = LLONG_MIN / 4;
    long long size = 1;
    while (size < n) size <<= 1;

    vector<Node> tr(size << 1);
    for (long long i = 0; i < (size << 1); ++i) {
        tr[i].sum = 0;
        tr[i].pre = NEG;
        tr[i].suf = NEG;
        tr[i].best = NEG;
    }
    for (long long i = 0; i < n; ++i) {
        Node& t = tr[size + i];
        t.sum = a[i];
        t.pre = a[i];
        t.suf = a[i];
        t.best = a[i];
    }
    for (long long k = size - 1; k >= 1; --k) tr[k] = mergeNode(tr[k << 1], tr[k << 1 | 1]);

    vector<long long> answer;
    for (long long j = 0; j < q; ++j) {
        long long l = size + ops[j][0] - 1;
        long long r = size + ops[j][1];
        Node L, R;
        while (l < r) {
            if (l & 1) {
                L = mergeNode(L, tr[l]);
                ++l;
            }
            if (r & 1) {
                --r;
                R = mergeNode(tr[r], R);
            }
            l >>= 1;
            r >>= 1;
        }
        answer.push_back(mergeNode(L, R).best);
    }
    return answer;
}
