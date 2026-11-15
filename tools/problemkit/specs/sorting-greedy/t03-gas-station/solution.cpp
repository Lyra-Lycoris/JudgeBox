#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& gas, const vector<long long>& cost) {
    long long total = 0;
    for (long long i = 0; i < n; ++i) total += gas[i] - cost[i];
    if (total < 0) return -1;
    long long start = 0, tank = 0;
    for (long long i = 0; i < n; ++i) {
        tank += gas[i] - cost[i];
        if (tank < 0) {
            start = i + 1;
            tank = 0;
        }
    }
    return start;
}
