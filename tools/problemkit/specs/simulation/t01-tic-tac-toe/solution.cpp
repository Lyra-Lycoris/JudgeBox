#include <bits/stdc++.h>
using namespace std;

const int LINES[8][3] = {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6},
                         {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}};

long long solve(const vector<long long>& moves) {
    long long board[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
    for (int step = 0; step < 9; ++step) {
        board[moves[step] - 1] = 1 + step % 2;
        for (int i = 0; i < 8; ++i) {
            long long a = board[LINES[i][0]];
            long long b = board[LINES[i][1]];
            long long c = board[LINES[i][2]];
            if (a != 0 && a == b && b == c) return step + 1;
        }
    }
    return 0;
}
