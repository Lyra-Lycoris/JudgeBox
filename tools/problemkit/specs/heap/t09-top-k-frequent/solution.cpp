#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long k, const vector<long long>& a) {
    unordered_map<long long, long long> count;
    for (long long x : a) count[x] += 1;
    vector<pair<long long, long long>> items;
    items.reserve(count.size());
    for (auto& entry : count) items.push_back(make_pair(-entry.second, entry.first));
    sort(items.begin(), items.end());
    vector<long long> answer;
    answer.reserve((size_t) k);
    for (long long i = 0; i < k; ++i) answer.push_back(items[(size_t) i].second);
    return answer;
}
