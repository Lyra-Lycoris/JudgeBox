#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& h) {
    long long left = 0, right = n - 1;
    long long leftMax = 0, rightMax = 0;
    long long water = 0;
    while (left <= right) {
        if (h[left] <= h[right]) {
            if (h[left] >= leftMax) leftMax = h[left];
            else water += leftMax - h[left];
            ++left;
        } else {
            if (h[right] >= rightMax) rightMax = h[right];
            else water += rightMax - h[right];
            --right;
        }
    }
    return water;
}
