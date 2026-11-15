#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a, long long m, const vector<vector<long long>>& queries) {
    vector<long long> values = a;
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    int uniq = (int)values.size();

    int depth = 1;
    while ((1LL << depth) < uniq) ++depth;
    int max_nodes = (int)(n * (depth + 1) + 2);

    vector<int> left_child((size_t)max_nodes, 0);
    vector<int> right_child((size_t)max_nodes, 0);
    vector<int> total((size_t)max_nodes, 0);
    vector<int> root((size_t)n + 1, 0);
    int nodes = 0;

    for (long long i = 0; i < n; ++i) {
        int pos = (int)(lower_bound(values.begin(), values.end(), a[(size_t)i]) - values.begin());
        int prev = root[(size_t)i];
        ++nodes;
        int node = nodes;
        total[node] = total[prev] + 1;
        left_child[node] = left_child[prev];
        right_child[node] = right_child[prev];
        root[(size_t)i + 1] = node;

        int lo = 0, hi = uniq - 1;
        int cur_new = node, cur_old = prev;
        while (lo < hi) {
            int mid = (lo + hi) >> 1;
            ++nodes;
            int child = nodes;
            if (pos <= mid) {
                int old_child = left_child[cur_old];
                total[child] = total[old_child] + 1;
                left_child[child] = left_child[old_child];
                right_child[child] = right_child[old_child];
                left_child[cur_new] = child;
                cur_new = child;
                cur_old = old_child;
                hi = mid;
            } else {
                int old_child = right_child[cur_old];
                total[child] = total[old_child] + 1;
                left_child[child] = left_child[old_child];
                right_child[child] = right_child[old_child];
                right_child[cur_new] = child;
                cur_new = child;
                cur_old = old_child;
                lo = mid + 1;
            }
        }
    }

    vector<long long> answer;
    answer.reserve((size_t)m);
    for (long long t = 0; t < m; ++t) {
        long long l = queries[(size_t)t][0];
        long long r = queries[(size_t)t][1];
        long long k = queries[(size_t)t][2];
        int root_r = root[(size_t)r];
        int root_l = root[(size_t)(l - 1)];
        int lo = 0, hi = uniq - 1;
        while (lo < hi) {
            int mid = (lo + hi) >> 1;
            int left_count = total[left_child[root_r]] - total[left_child[root_l]];
            if (k <= left_count) {
                root_r = left_child[root_r];
                root_l = left_child[root_l];
                hi = mid;
            } else {
                k -= left_count;
                root_r = right_child[root_r];
                root_l = right_child[root_l];
                lo = mid + 1;
            }
        }
        answer.push_back(values[(size_t)lo]);
    }
    return answer;
}
