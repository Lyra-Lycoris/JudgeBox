#include <bits/stdc++.h>
using namespace std;

long long solve(long long k, const vector<string>& words) {
    size_t limit = words[0].size();
    for (const string& w : words) limit = min(limit, w.size());
    size_t i = 0;
    while (i < limit) {
        char ch = words[0][i];
        bool ok = true;
        for (const string& w : words) {
            if (w[i] != ch) {
                ok = false;
                break;
            }
        }
        if (!ok) break;
        ++i;
    }
    return (long long)i;
}
