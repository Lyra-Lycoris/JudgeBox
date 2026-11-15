#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    vector<long long> values = a;
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    long long m = (long long)values.size();
    vector<long long> tree(m + 1, 0);
    long long answer = 0;
    for (long long k = 0; k < n; ++k) {
        long long p = lower_bound(values.begin(), values.end(), a[k]) - values.begin() + 1;
        long long notGreater = 0;
        for (long long i = p; i > 0; i -= i & -i) notGreater += tree[i];
        answer += k - notGreater;
        for (long long i = p; i <= m; i += i & -i) tree[i] += 1;
    }
    return answer;
}
