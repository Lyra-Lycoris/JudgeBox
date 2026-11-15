#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<vector<long long>>& g) {
    long long best = 0;
    vector<long long> heights(m, 0);
    vector<long long> st;
    for (long long top = 0; top < n; ++top) {
        fill(heights.begin(), heights.end(), 0);
        for (long long bottom = top; bottom < n; ++bottom) {
            for (long long c = 0; c < m; ++c) {
                heights[c] = (g[bottom][c] != 0) ? heights[c] + 1 : 0;
            }
            st.clear();
            for (long long c = 0; c <= m; ++c) {
                long long h = (c < m) ? heights[c] : 0;
                while (!st.empty() && heights[st.back()] >= h) {
                    long long ph = heights[st.back()];
                    st.pop_back();
                    long long left = st.empty() ? -1 : st.back();
                    long long area = ph * (c - left - 1);
                    if (area > best) best = area;
                }
                st.push_back(c);
            }
        }
    }
    return best;
}
