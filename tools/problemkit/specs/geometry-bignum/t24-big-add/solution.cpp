#include <bits/stdc++.h>
using namespace std;

string solve(string a, string b) {
    int i = (int)a.size() - 1;
    int j = (int)b.size() - 1;
    int carry = 0;
    string result;
    result.reserve((size_t)max(a.size(), b.size()) + 1);
    while (i >= 0 || j >= 0 || carry > 0) {
        int sum = carry;
        if (i >= 0) {
            sum += a[i] - '0';
            --i;
        }
        if (j >= 0) {
            sum += b[j] - '0';
            --j;
        }
        result.push_back((char)('0' + sum % 10));
        carry = sum / 10;
    }
    reverse(result.begin(), result.end());
    return result;
}
