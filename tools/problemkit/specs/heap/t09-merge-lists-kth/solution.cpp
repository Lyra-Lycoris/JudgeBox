#include <bits/stdc++.h>
using namespace std;

long long solve(long long k, long long m, long long t, const vector<vector<long long>>& lists) {
    priority_queue<tuple<long long, long long, long long>,
                   vector<tuple<long long, long long, long long>>,
                   greater<tuple<long long, long long, long long>>> heap;
    for (long long r = 0; r < k; ++r) heap.push(make_tuple(lists[r][0], r, 0LL));
    long long answer = 0;
    for (long long step = 0; step < t; ++step) {
        tuple<long long, long long, long long> cur = heap.top();
        heap.pop();
        long long value = get<0>(cur);
        long long r = get<1>(cur);
        long long c = get<2>(cur);
        answer = value;
        if (c + 1 < m) heap.push(make_tuple(lists[r][c + 1], r, c + 1));
    }
    return answer;
}
