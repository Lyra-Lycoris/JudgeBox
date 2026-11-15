#include <bits/stdc++.h>
using namespace std;

static long long powMod(long long base, long long exp) {
    const long long MOD = 1000000007LL;
    long long result = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp & 1LL) result = result * base % MOD;
        base = base * base % MOD;
        exp >>= 1;
    }
    return result;
}

static long long norm(long long value) {
    const long long MOD = 1000000007LL;
    long long r = value % MOD;
    if (r < 0) r += MOD;
    return r;
}

long long solve(long long n, const vector<long long>& a) {
    const long long MOD = 1000000007LL;
    if (n < 2) return 0;

    vector<long long> uniq(a.begin(), a.end());
    sort(uniq.begin(), uniq.end());
    uniq.erase(unique(uniq.begin(), uniq.end()), uniq.end());
    long long m = (long long)uniq.size();

    vector<long long> cnt(m, 0), lessCnt(m, 0), greaterCnt(m, 0);
    for (long long i = 0; i < n; ++i) {
        long long idx = lower_bound(uniq.begin(), uniq.end(), a[i]) - uniq.begin();
        cnt[idx]++;
    }
    long long running = 0;
    for (long long i = 0; i < m; ++i) {
        lessCnt[i] = running;
        running += cnt[i];
    }
    for (long long i = 0; i < m; ++i) {
        greaterCnt[i] = n - lessCnt[i] - cnt[i];
    }

    vector<long long> tree(m + 1, 0);
    long long invCount = 0;
    for (long long k = 0; k < n; ++k) {
        long long r = (lower_bound(uniq.begin(), uniq.end(), a[k]) - uniq.begin()) + 1;
        long long seen = 0;
        for (long long i = r; i > 0; i -= i & -i) seen += tree[i];
        invCount += k - seen;
        for (long long i = r; i <= m; i += i & -i) tree[i]++;
    }

    long long equalPairs = 0;
    for (long long i = 0; i < m; ++i) {
        equalPairs += cnt[i] * (cnt[i] - 1) / 2;
    }
    long long totalPairs = n * (n - 1) / 2;
    long long untouched = (n - 2) * (n - 3) / 2;

    long long total = norm((untouched % MOD) * (invCount % MOD));
    total = norm(total + norm((totalPairs % MOD) - (invCount % MOD) - (equalPairs % MOD)));

    long long sumLeft = 0;
    for (long long k = 0; k < n; ++k) {
        long long idx = lower_bound(uniq.begin(), uniq.end(), a[k]) - uniq.begin();
        sumLeft = norm(sumLeft + norm((k % MOD) * (greaterCnt[idx] % MOD)));
    }
    total = norm(total + sumLeft);

    long long sumRight = 0;
    for (long long k = 0; k < n; ++k) {
        long long idx = lower_bound(uniq.begin(), uniq.end(), a[k]) - uniq.begin();
        sumRight = norm(sumRight + norm(((n - 1 - k) % MOD) * (lessCnt[idx] % MOD)));
    }
    total = norm(total + sumRight);

    total = norm(total - 2 * (invCount % MOD) % MOD);
    return norm(total * powMod(totalPairs % MOD, MOD - 2));
}
