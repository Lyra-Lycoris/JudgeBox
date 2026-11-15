#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    unordered_map<long long, long long> diffCounts, sumCounts;
    diffCounts.reserve(a.size() * 2 + 16);
    sumCounts.reserve(a.size() * 2 + 16);
    long long answer = 0;
    for (long long i = 0; i < n; ++i) {
        long long index = i + 1;
        long long& diffSeen = diffCounts[a[i] - index];
        answer += diffSeen;
        diffSeen += 1;
        long long& sumSeen = sumCounts[a[i] + index];
        answer += sumSeen;
        sumSeen += 1;
    }
    return answer;
}
