#include <bits/stdc++.h>
using namespace std;

static long long mergeCount(vector<long long>& a, vector<long long>& tmp, int l, int r) {
    if (r - l <= 1) return 0;
    int mid = (l + r) / 2;
    long long total = mergeCount(a, tmp, l, mid) + mergeCount(a, tmp, mid, r);
    int i = l, j = mid, k = l;
    while (i < mid && j < r) {
        if (a[i] <= a[j]) {
            tmp[k++] = a[i++];
        } else {
            tmp[k++] = a[j++];
            total += mid - i;
        }
    }
    while (i < mid) tmp[k++] = a[i++];
    while (j < r) tmp[k++] = a[j++];
    for (int p = l; p < r; ++p) a[p] = tmp[p];
    return total;
}

long long solve(long long n, const vector<long long>& a) {
    vector<long long> work(a.begin(), a.end());
    vector<long long> tmp((size_t)n);
    return mergeCount(work, tmp, 0, (int)n);
}
