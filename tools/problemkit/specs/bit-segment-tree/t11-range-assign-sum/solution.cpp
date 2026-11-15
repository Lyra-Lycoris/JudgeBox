#include <bits/stdc++.h>
using namespace std;

namespace assign_sum {

const long long NONE = LLONG_MAX;
vector<long long> treeSum;
vector<long long> treeTag;

void build(long long node, long long l, long long r, const vector<long long>& a) {
    treeTag[node] = NONE;
    if (l == r) {
        treeSum[node] = a[l - 1];
        return;
    }
    long long mid = (l + r) / 2;
    build(node * 2, l, mid, a);
    build(node * 2 + 1, mid + 1, r, a);
    treeSum[node] = treeSum[node * 2] + treeSum[node * 2 + 1];
}

void applyNode(long long node, long long l, long long r, long long v) {
    treeSum[node] = v * (r - l + 1);
    treeTag[node] = v;
}

void pushDown(long long node, long long l, long long r) {
    if (treeTag[node] == NONE || l == r) return;
    long long mid = (l + r) / 2;
    applyNode(node * 2, l, mid, treeTag[node]);
    applyNode(node * 2 + 1, mid + 1, r, treeTag[node]);
    treeTag[node] = NONE;
}

void update(long long node, long long l, long long r, long long ql, long long qr, long long v) {
    if (ql <= l && r <= qr) {
        applyNode(node, l, r, v);
        return;
    }
    pushDown(node, l, r);
    long long mid = (l + r) / 2;
    if (ql <= mid) update(node * 2, l, mid, ql, qr, v);
    if (qr > mid) update(node * 2 + 1, mid + 1, r, ql, qr, v);
    treeSum[node] = treeSum[node * 2] + treeSum[node * 2 + 1];
}

}  // namespace assign_sum

vector<long long> solve(long long n, const vector<long long>& a, long long q,
                        const vector<vector<long long>>& ops) {
    using namespace assign_sum;
    treeSum.assign(4 * n + 4, 0);
    treeTag.assign(4 * n + 4, 0);
    build(1, 1, n, a);
    vector<long long> answer;
    for (long long j = 0; j < q; ++j) {
        update(1, 1, n, ops[j][0], ops[j][1], ops[j][2]);
        answer.push_back(treeSum[1]);
    }
    return answer;
}
