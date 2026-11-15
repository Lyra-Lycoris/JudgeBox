#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long c, const vector<long long>& tasks) {
    unordered_map<long long, long long> count;
    for (long long x : tasks) count[x] += 1;
    priority_queue<long long> heap;
    for (auto& entry : count) heap.push(entry.second);
    long long time = 0;
    while (!heap.empty()) {
        long long slot = min<long long>(c + 1, (long long) heap.size());
        vector<long long> rest;
        for (long long i = 0; i < slot; ++i) {
            long long top = heap.top();
            heap.pop();
            if (top > 1) rest.push_back(top - 1);
        }
        time += c + 1;
        for (long long x : rest) heap.push(x);
        if (heap.empty()) time -= c + 1 - slot;
    }
    return time;
}
