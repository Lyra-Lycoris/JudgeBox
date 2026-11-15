#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a, long long q, const vector<vector<long long>>& ops) {
    vector<long long> values = a;
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    int m = (int)values.size();

    vector<int> comp((size_t)n);
    for (long long i = 0; i < n; ++i) {
        comp[(size_t)i] = (int)(lower_bound(values.begin(), values.end(), a[(size_t)i]) - values.begin());
    }
    vector<vector<int>> pos(m);
    for (long long i = 0; i < n; ++i) {
        pos[comp[(size_t)i]].push_back((int)i);
    }

    int B = max(1, (int)(sqrt((double)n) + 1e-9));
    int nb = (int)((n + B - 1) / B);

    vector<vector<int>> table_c(nb, vector<int>(nb, 0));
    vector<vector<int>> table_v(nb, vector<int>(nb, -1));
    vector<int> cnt(m, 0);
    for (int s = 0; s < nb; ++s) {
        fill(cnt.begin(), cnt.end(), 0);
        int bc = 0, bv = -1;
        for (long long i = (long long)s * B; i < n; ++i) {
            int v = comp[(size_t)i];
            int c = ++cnt[v];
            if (c > bc || (c == bc && v < bv)) {
                bc = c;
                bv = v;
            }
            if ((i + 1) % B == 0 || i == n - 1) {
                int j = (int)(i / B);
                table_c[s][j] = bc;
                table_v[s][j] = bv;
            }
        }
    }

    vector<long long> answer;
    answer.reserve((size_t)q);
    vector<int> cnt2(m, 0);
    vector<int> touched;
    touched.reserve((size_t)B + 1);

    for (long long t = 0; t < q; ++t) {
        int l = (int)(ops[(size_t)t][0] - 1);
        int r = (int)(ops[(size_t)t][1] - 1);
        int bl = l / B, br = r / B;
        int bc, bv;
        if (bl == br) {
            bc = 0;
            bv = -1;
            touched.clear();
            for (int i = l; i <= r; ++i) {
                int v = comp[(size_t)i];
                if (cnt2[v] == 0) touched.push_back(v);
                int c = ++cnt2[v];
                if (c > bc || (c == bc && v < bv)) {
                    bc = c;
                    bv = v;
                }
            }
            for (int v : touched) cnt2[v] = 0;
        } else {
            if (bl + 1 < br) {
                bc = table_c[bl + 1][br - 1];
                bv = table_v[bl + 1][br - 1];
            } else {
                bc = 0;
                bv = -1;
            }
            int end = (bl + 1) * B;
            for (int i = l; i < end; ++i) {
                int v = comp[(size_t)i];
                const vector<int>& p = pos[v];
                int c = (int)(upper_bound(p.begin(), p.end(), r) - lower_bound(p.begin(), p.end(), l));
                if (c > bc || (c == bc && v < bv)) {
                    bc = c;
                    bv = v;
                }
            }
            for (int i = br * B; i <= r; ++i) {
                int v = comp[(size_t)i];
                const vector<int>& p = pos[v];
                int c = (int)(upper_bound(p.begin(), p.end(), r) - lower_bound(p.begin(), p.end(), l));
                if (c > bc || (c == bc && v < bv)) {
                    bc = c;
                    bv = v;
                }
            }
        }
        answer.push_back(values[(size_t)bv]);
    }
    return answer;
}
