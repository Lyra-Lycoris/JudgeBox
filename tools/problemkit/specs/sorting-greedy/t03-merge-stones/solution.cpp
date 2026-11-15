#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    if (n <= 1) return 0;
    priority_queue<long long, vector<long long>, greater<long long>> pq(a.begin(), a.end());
    long long total = 0;
    while (pq.size() > 1) {
        long long x = pq.top();
        pq.pop();
        long long y = pq.top();
        pq.pop();
        total += x + y;
        pq.push(x + y);
    }
    return total;
}
