#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, string s) {
    long long counts[26] = {0};
    for (char c : s) counts[c - 'a'] += 1;
    for (long long i = 0; i < (long long)s.size(); ++i)
        if (counts[s[i] - 'a'] == 1) return i + 1;
    return -1;
}
