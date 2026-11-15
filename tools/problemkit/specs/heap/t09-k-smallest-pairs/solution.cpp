#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long m, long long k, const vector<long long>& a,
                        const vector<long long>& b) {
    priority_queue<tuple<long long, long long, long long>,
                   vector<tuple<long long, long long, long long>>,
                   greater<tuple<long long, long long, long long>>> heap;
    heap.push(make_tuple(a[0] + b[0], 0LL, 0LL));
    vector<long long> answer;
    answer.reserve((size_t) k);
    while ((long long) answer.size() < k) {
        tuple<long long, long long, long long> cur = heap.top();
        heap.pop();
        long long sum = get<0>(cur);
        long long i = get<1>(cur);
        long long j = get<2>(cur);
        answer.push_back(sum);
        if (i + 1 < n) heap.push(make_tuple(a[i + 1] + b[j], i + 1, j));
        if (i == 0 && j + 1 < m) heap.push(make_tuple(a[i] + b[j + 1], i, j + 1));
    }
    return answer;
}
