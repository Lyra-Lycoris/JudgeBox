#include <bits/stdc++.h>
using namespace std;

long long solve(long long l, long long r) {
    long long power[17];
    power[0] = 1;
    for (int i = 1; i < 17; ++i) power[i] = power[i - 1] * 10;
    long long suffix[17];
    suffix[0] = 0;
    for (int i = 1; i < 17; ++i) suffix[i] = (long long)i * 45 * power[i - 1];

    auto totalUpTo = [&](long long x) -> long long {
        if (x < 0) return 0;
        vector<int> digits;
        long long t = x;
        while (true) {
            digits.push_back((int)(t % 10));
            t /= 10;
            if (t == 0) break;
        }
        int len = (int)digits.size();
        long long result = 0;
        long long prefix = 0;
        for (int pos = len - 1; pos >= 0; --pos) {
            int cur = digits[pos];
            for (int v = 0; v < cur; ++v) {
                result += (prefix + v) * power[pos] + suffix[pos];
            }
            prefix += cur;
        }
        return result + prefix;
    };
    return totalUpTo(r) - totalUpTo(l - 1);
}
