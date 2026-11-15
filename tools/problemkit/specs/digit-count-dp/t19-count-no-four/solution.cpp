#include <bits/stdc++.h>
using namespace std;

long long solve(long long l, long long r) {
    auto countNoFour = [](long long x) -> long long {
        if (x < 0) return 0;
        vector<int> digits;
        long long t = x;
        while (true) {
            digits.push_back((int)(t % 10));
            t /= 10;
            if (t == 0) break;
        }
        int len = (int)digits.size();
        long long power[20];
        power[0] = 1;
        for (int i = 1; i <= len; ++i) power[i] = power[i - 1] * 9;
        long long total = 0;
        for (int pos = len - 1; pos >= 0; --pos) {
            int cur = digits[pos];
            long long smaller = 0;
            for (int v = 0; v < cur; ++v) {
                if (v != 4) ++smaller;
            }
            total += smaller * power[pos];
            if (cur == 4) return total;
        }
        return total + 1;
    };
    return countNoFour(r) - countNoFour(l - 1);
}
