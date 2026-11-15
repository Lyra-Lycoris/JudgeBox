#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    vector<pair<long long, long long>> p(n);
    for (long long i = 0; i < n; ++i) p[i] = make_pair(a[i], i);
    sort(p.begin(), p.end());
    vector<long long> bit(n + 1, 0);
    long long answer = 0;
    long long seen = 0;
    for (long long k = 0; k < n; ++k) {
        long long pos = p[k].second + 1;
        long long s = 0;
        for (long long t = pos; t > 0; t -= t & (-t)) s += bit[t];
        answer += seen - s;
        ++seen;
        for (long long t = pos; t <= n; t += t & (-t)) ++bit[t];
    }
    return answer;
}
