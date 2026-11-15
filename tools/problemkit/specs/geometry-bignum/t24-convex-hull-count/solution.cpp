#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& xs, const vector<long long>& ys) {
    vector<pair<long long, long long>> pts;
    pts.reserve((size_t)n);
    for (long long i = 0; i < n; ++i) pts.push_back(make_pair(xs[i], ys[i]));
    sort(pts.begin(), pts.end());
    pts.erase(unique(pts.begin(), pts.end()), pts.end());
    long long m = (long long)pts.size();
    if (m <= 2) return m;

    auto turn = [](const pair<long long, long long>& o,
                   const pair<long long, long long>& a,
                   const pair<long long, long long>& b) -> long long {
        return (a.first - o.first) * (b.second - o.second) -
               (a.second - o.second) * (b.first - o.first);
    };

    vector<pair<long long, long long>> lower;
    for (long long i = 0; i < m; ++i) {
        while (lower.size() >= 2 && turn(lower[lower.size() - 2], lower.back(), pts[i]) <= 0) {
            lower.pop_back();
        }
        lower.push_back(pts[i]);
    }
    vector<pair<long long, long long>> upper;
    for (long long i = m - 1; i >= 0; --i) {
        while (upper.size() >= 2 && turn(upper[upper.size() - 2], upper.back(), pts[i]) <= 0) {
            upper.pop_back();
        }
        upper.push_back(pts[i]);
    }
    return (long long)lower.size() + (long long)upper.size() - 2;
}
