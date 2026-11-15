#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long k, const vector<long long>& a) {
    deque<long long> window;
    vector<long long> answer;
    answer.reserve(n - k + 1);
    for (long long i = 0; i < n; ++i) {
        while (!window.empty() && a[window.back()] <= a[i]) window.pop_back();
        window.push_back(i);
        if (window.front() <= i - k) window.pop_front();
        if (i >= k - 1) answer.push_back(a[window.front()]);
    }
    return answer;
}
