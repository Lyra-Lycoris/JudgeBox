#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long k, const vector<long long>& p) {
    vector<long long> perm(n);
    for (long long i = 0; i < n; ++i) perm[i] = p[i] - 1;
    vector<long long> answer(n, 0);
    vector<char> visited(n, 0);
    vector<long long> cycle;
    for (long long start = 0; start < n; ++start) {
        if (visited[start]) continue;
        cycle.clear();
        long long current = start;
        while (!visited[current]) {
            visited[current] = 1;
            cycle.push_back(current);
            current = perm[current];
        }
        long long length = (long long)cycle.size();
        long long shift = k % length;
        for (long long j = 0; j < length; ++j) {
            long long source = (j - shift) % length;
            if (source < 0) source += length;
            answer[cycle[j]] = cycle[source] + 1;
        }
    }
    return answer;
}
