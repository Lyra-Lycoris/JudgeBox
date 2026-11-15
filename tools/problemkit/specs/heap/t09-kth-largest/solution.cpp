#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long k, const vector<long long>& a) {
    priority_queue<long long, vector<long long>, greater<long long>> heap;
    for (long long x : a) {
        heap.push(x);
        if ((long long) heap.size() > k) heap.pop();
    }
    return heap.top();
}
