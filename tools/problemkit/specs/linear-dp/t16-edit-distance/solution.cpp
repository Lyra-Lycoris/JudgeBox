#include <bits/stdc++.h>
using namespace std;

long long solve(string s, string t) {
    int n = (int)s.size();
    int m = (int)t.size();
    vector<int> prev(m + 1), cur(m + 1);
    for (int j = 0; j <= m; ++j) prev[j] = j;
    for (int i = 1; i <= n; ++i) {
        cur[0] = i;
        for (int j = 1; j <= m; ++j) {
            int best = min(prev[j] + 1, cur[j - 1] + 1);
            int sub = prev[j - 1] + (s[i - 1] == t[j - 1] ? 0 : 1);
            if (sub < best) best = sub;
            cur[j] = best;
        }
        swap(prev, cur);
    }
    return prev[m];
}
