#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& p) {
    vector<long long> size(n + 1, 1);
    size[0] = 0;
    for (long long v = n; v >= 2; --v) {
        size[p[v - 2]] += size[v];
    }
    vector<long long> answer(n);
    for (long long i = 1; i <= n; ++i) answer[i - 1] = size[i];
    return answer;
}
