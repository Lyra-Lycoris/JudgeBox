#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<long long>& s,
                const vector<long long>& d) {
    vector<long long> order((size_t) m);
    for (long long i = 0; i < m; ++i) order[(size_t) i] = i;
    sort(order.begin(), order.end(), [&](long long x, long long y) {
        if (s[(size_t) x] != s[(size_t) y]) return s[(size_t) x] < s[(size_t) y];
        return x < y;
    });
    vector<long long> used((size_t) n, 0);
    priority_queue<long long, vector<long long>, greater<long long>> free;
    for (long long i = n - 1; i >= 0; --i) free.push(i);
    priority_queue<pair<long long, long long>, vector<pair<long long, long long>>,
                   greater<pair<long long, long long>>> busy;
    for (long long idx : order) {
        long long start = s[(size_t) idx];
        while (!busy.empty() && busy.top().first <= start) {
            free.push(busy.top().second);
            busy.pop();
        }
        long long room;
        if (!free.empty()) {
            room = free.top();
            free.pop();
            busy.push(make_pair(start + d[(size_t) idx], room));
        } else {
            pair<long long, long long> cur = busy.top();
            busy.pop();
            room = cur.second;
            busy.push(make_pair(cur.first + d[(size_t) idx], room));
        }
        used[(size_t) room] += 1;
    }
    long long best = 0;
    for (long long i = 1; i < n; ++i) {
        if (used[(size_t) i] > used[(size_t) best]) best = i;
    }
    return best;
}
