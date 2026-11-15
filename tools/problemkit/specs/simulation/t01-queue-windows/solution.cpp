#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long k, const vector<long long>& arrive, const vector<long long>& serve) {
    priority_queue<long long, vector<long long>, greater<long long>> freeAt;
    for (long long i = 0; i < k; ++i) freeAt.push(0);
    long long total = 0;
    for (long long i = 0; i < n; ++i) {
        long long free = freeAt.top();
        freeAt.pop();
        long long start = max(free, arrive[i]);
        total += start - arrive[i];
        freeAt.push(start + serve[i]);
    }
    return total;
}
