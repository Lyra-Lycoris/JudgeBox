#include <bits/stdc++.h>
using namespace std;

long long solve(long long n) {
    if (n < 10) return n;
    string s = to_string(n);
    int L = static_cast<int>(s.size());
    string half = s.substr(0, (L + 1) / 2);

    string rev = half.substr(0, L / 2);
    reverse(rev.begin(), rev.end());
    long long candidate = stoll(half + rev);
    if (candidate >= n) return candidate;

    string next = half;
    int i = static_cast<int>(next.size()) - 1;
    while (i >= 0 && next[i] == '9') {
        next[i] = '0';
        --i;
    }
    if (i < 0) {
        string answer = "1";
        answer += string(L - 1, '0');
        answer += "1";
        return stoll(answer);
    }
    next[i] += 1;

    string rev2 = next.substr(0, L / 2);
    reverse(rev2.begin(), rev2.end());
    return stoll(next + rev2);
}
