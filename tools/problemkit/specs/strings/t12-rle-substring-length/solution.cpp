#include <bits/stdc++.h>
using namespace std;

static long long encodedCost(long long length) {
    if (length <= 1) return 1;
    long long value = length;
    long long digits = 0;
    while (value > 0) {
        ++digits;
        value /= 10;
    }
    return 1 + digits;
}

vector<long long> solve(long long n, string s, long long q, const vector<vector<long long>>& qs) {
    long long m = (long long)s.size();
    vector<long long> runEnd;
    runEnd.reserve((size_t)m + 1);
    vector<long long> prefix;
    prefix.push_back(0);
    long long index = 0;
    while (index < m) {
        long long j = index;
        while (j < m && s[(size_t)j] == s[(size_t)index]) ++j;
        runEnd.push_back(j);
        prefix.push_back(prefix.back() + encodedCost(j - index));
        index = j;
    }
    vector<long long> answer((size_t)q, 0);
    for (long long k = 0; k < q; ++k) {
        long long left = qs[(size_t)k][0];
        long long right = qs[(size_t)k][1];
        long long low = (long long)(upper_bound(runEnd.begin(), runEnd.end(), left - 1) - runEnd.begin());
        long long high = (long long)(upper_bound(runEnd.begin(), runEnd.end(), right - 1) - runEnd.begin());
        if (low == high) {
            answer[(size_t)k] = encodedCost(right - left + 1);
        } else {
            long long total = encodedCost(runEnd[(size_t)low] - (left - 1));
            total += encodedCost(right - runEnd[(size_t)(high - 1)]);
            total += prefix[(size_t)high] - prefix[(size_t)(low + 1)];
            answer[(size_t)k] = total;
        }
    }
    return answer;
}
