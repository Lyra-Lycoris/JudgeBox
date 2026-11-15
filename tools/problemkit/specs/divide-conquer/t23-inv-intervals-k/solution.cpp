#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long k, const vector<long long>& a) {
    if (k <= 0) return n * (n + 1) / 2;
    vector<long long> values(a.begin(), a.end());
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    int m = (int)values.size();
    vector<long long> tree(m + 1, 0);
    auto add = [&](int pos, long long delta) {
        for (int i = pos; i <= m; i += i & -i) tree[i] += delta;
    };
    auto prefix = [&](int pos) {
        long long sum = 0;
        for (int i = pos; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    };
    long long answer = 0;
    long long windowSize = 0;
    long long inversions = 0;
    int right = 0;
    for (int left = 0; left < (int)n; ++left) {
        while (right < (int)n && inversions < k) {
            int pos = (int)(lower_bound(values.begin(), values.end(), a[right]) - values.begin()) + 1;
            inversions += windowSize - prefix(pos);
            add(pos, 1);
            windowSize += 1;
            right += 1;
        }
        if (inversions >= k) answer += n - right + 1;
        int pos = (int)(lower_bound(values.begin(), values.end(), a[left]) - values.begin()) + 1;
        inversions -= prefix(pos - 1);
        add(pos, -1);
        windowSize -= 1;
    }
    return answer;
}
