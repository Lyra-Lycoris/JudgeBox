#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a, long long k) {
    vector<long long> rems(n + 1, 0);
    long long cur = 0;
    for (long long i = 0; i < n; ++i) {
        cur = (cur + a[i]) % k;
        if (cur < 0) cur += k;
        rems[i + 1] = cur;
    }
    sort(rems.begin(), rems.end());
    long long answer = 0;
    long long run = 1;
    for (long long i = 1; i <= n; ++i) {
        if (rems[i] == rems[i - 1]) {
            ++run;
        } else {
            answer += run * (run - 1) / 2;
            run = 1;
        }
    }
    answer += run * (run - 1) / 2;
    return answer;
}
