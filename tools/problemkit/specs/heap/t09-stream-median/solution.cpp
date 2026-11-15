#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a) {
    priority_queue<long long> low;
    priority_queue<long long, vector<long long>, greater<long long>> high;
    vector<long long> answer;
    answer.reserve((size_t) n);
    for (long long i = 0; i < n; ++i) {
        long long x = a[(size_t) i];
        if (low.empty() || x <= low.top()) low.push(x);
        else high.push(x);
        long long target = (i + 2) / 2;
        while ((long long) low.size() > target) {
            high.push(low.top());
            low.pop();
        }
        while ((long long) low.size() < target) {
            low.push(high.top());
            high.pop();
        }
        answer.push_back(low.top());
    }
    return answer;
}
