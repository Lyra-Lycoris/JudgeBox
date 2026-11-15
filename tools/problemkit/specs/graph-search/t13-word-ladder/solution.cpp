#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, string begin, string end, const vector<string>& w) {
    int N = (int) n;
    if (begin == end) return 1;
    int target = -1, bidx = -1;
    for (int i = 0; i < N; ++i) {
        if (target < 0 && w[i] == end) target = i;
        if (bidx < 0 && w[i] == begin) bidx = i;
    }
    if (target < 0) return 0;

    unordered_map<string, vector<int>> buckets;
    buckets.reserve((size_t) N * 8 + 8);
    for (int i = 0; i < N; ++i) {
        string key = w[i];
        for (size_t j = 0; j < key.size(); ++j) {
            char old = key[j];
            key[j] = '*';
            buckets[key].push_back(i);
            key[j] = old;
        }
    }

    vector<long long> dist((size_t) N + 1, -1);
    dist[N] = 1;
    if (bidx >= 0) dist[bidx] = 1;
    vector<int> queue;
    queue.reserve((size_t) N + 1);
    queue.push_back(N);
    size_t head = 0;
    while (head < queue.size()) {
        int u = queue[head++];
        long long step = dist[u] + 1;
        string word = (u == N) ? begin : w[u];
        for (size_t j = 0; j < word.size(); ++j) {
            char old = word[j];
            word[j] = '*';
            auto it = buckets.find(word);
            word[j] = old;
            if (it == buckets.end()) continue;
            vector<int> group = std::move(it->second);
            buckets.erase(it);
            for (int v : group) {
                if (dist[v] != -1) continue;
                dist[v] = step;
                if (v == target) return step;
                queue.push_back(v);
            }
        }
    }
    return 0;
}
