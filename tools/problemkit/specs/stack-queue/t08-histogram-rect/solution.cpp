#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& h) {
    vector<long long> stack;
    stack.reserve(n + 1);
    long long best = 0;
    for (long long i = 0; i <= n; ++i) {
        long long cur = (i < n) ? h[i] : 0;
        while (!stack.empty() && h[stack.back()] >= cur) {
            long long height = h[stack.back()];
            stack.pop_back();
            long long left = stack.empty() ? -1 : stack.back();
            best = max(best, height * (i - left - 1));
        }
        stack.push_back(i);
    }
    return best;
}
