#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    if (n <= 1) return 0;
    priority_queue<long long, vector<long long>, greater<long long>> heap(a.begin(), a.end());
    long long total = 0;
    for (long long x : a) total += x;
    long long cost = 0;
    while (heap.size() > 1) {
        long long x = heap.top();
        heap.pop();
        long long y = heap.top();
        heap.pop();
        cost += x + y;
        heap.push(x + y);
    }
    return cost - total;
}
