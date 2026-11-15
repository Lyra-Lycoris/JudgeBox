#include <bits/stdc++.h>
using namespace std;

string solve(string a, string b) {
    if (a == "0" || b == "0") return "0";
    int la = (int)a.size();
    int lb = (int)b.size();
    vector<long long> acc((size_t)la + (size_t)lb, 0);
    for (int i = la - 1; i >= 0; --i) {
        long long da = a[i] - '0';
        for (int j = lb - 1; j >= 0; --j) {
            acc[(size_t)i + (size_t)j + 1] += da * (b[j] - '0');
        }
    }
    for (int k = (int)acc.size() - 1; k > 0; --k) {
        acc[(size_t)k - 1] += acc[(size_t)k] / 10;
        acc[(size_t)k] %= 10;
    }
    size_t start = 0;
    while (start + 1 < acc.size() && acc[start] == 0) ++start;
    string result;
    result.reserve(acc.size() - start);
    for (size_t k = start; k < acc.size(); ++k) result.push_back((char)('0' + acc[k]));
    return result;
}
