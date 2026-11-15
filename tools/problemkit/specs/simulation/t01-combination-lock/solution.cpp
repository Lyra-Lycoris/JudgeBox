#include <bits/stdc++.h>
using namespace std;

int parseCode(const string& text) {
    return (text[0] - '0') * 1000 + (text[1] - '0') * 100 + (text[2] - '0') * 10 + (text[3] - '0');
}

long long solve(string start, string target, long long n, const vector<string>& dead) {
    vector<char> blocked(10000, 0);
    for (const string& code : dead) blocked[parseCode(code)] = 1;
    int begin = parseCode(start);
    int goal = parseCode(target);
    if (blocked[begin] || blocked[goal]) return -1;
    if (begin == goal) return 0;
    vector<int> dist(10000, -1);
    vector<int> queue(10000, 0);
    int head = 0, tail = 0;
    dist[begin] = 0;
    queue[tail++] = begin;
    const int power[4] = {1, 10, 100, 1000};
    while (head < tail) {
        int cur = queue[head++];
        int step = dist[cur] + 1;
        for (int p : power) {
            int digit = (cur / p) % 10;
            int nexts[2] = {(digit + 1) % 10, (digit + 9) % 10};
            for (int nd : nexts) {
                int nxt = cur + (nd - digit) * p;
                if (dist[nxt] == -1 && !blocked[nxt]) {
                    dist[nxt] = step;
                    if (nxt == goal) return step;
                    queue[tail++] = nxt;
                }
            }
        }
    }
    return -1;
}
