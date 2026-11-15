#include <bits/stdc++.h>
using namespace std;

long long solve(long long l, long long r, long long k) {
    static long long cnt[19][10];
    for (int last = 0; last < 10; ++last) cnt[0][last] = 1;
    for (int rem = 1; rem < 19; ++rem) {
        for (int last = 0; last < 10; ++last) {
            long long sum = 0;
            for (int v = 0; v < 10; ++v) {
                if (llabs((long long)v - last) <= k) sum += cnt[rem - 1][v];
            }
            cnt[rem][last] = sum;
        }
    }

    auto countUpTo = [&](long long x) -> long long {
        if (x <= 0) return 0;
        vector<int> digits;
        long long t = x;
        while (true) {
            digits.push_back((int)(t % 10));
            t /= 10;
            if (t == 0) break;
        }
        int len = (int)digits.size();
        long long res = 0;
        for (int length = 1; length < len; ++length) {
            for (int first = 1; first <= 9; ++first) res += cnt[length - 1][first];
        }
        for (int pos = len - 1; pos >= 0; --pos) {
            int lo = (pos == len - 1) ? 1 : 0;
            for (int v = lo; v < digits[pos]; ++v) {
                if (pos < len - 1 && llabs((long long)v - digits[pos + 1]) > k) continue;
                res += cnt[pos][v];
            }
            if (pos < len - 1 && llabs((long long)digits[pos] - digits[pos + 1]) > k) return res;
        }
        return res + 1;
    };

    return countUpTo(r) - countUpTo(l - 1);
}
