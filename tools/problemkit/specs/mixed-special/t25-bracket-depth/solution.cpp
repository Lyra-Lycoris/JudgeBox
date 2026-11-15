#include <bits/stdc++.h>
using namespace std;

string solve(long long n, long long k) {
    string s;
    s.reserve((size_t)n);
    s.append((size_t)k, '(');
    s.append((size_t)k, ')');
    for (long long i = 0; i < (n - 2 * k) / 2; ++i) s += "()";
    return s;
}
