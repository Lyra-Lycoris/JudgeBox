#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long target, const vector<long long>& a) {
    long long i = 0, j = n - 1, count = 0;
    while (i < j) {
        long long sum = a[i] + a[j];
        if (sum < target) {
            i++;
        } else if (sum > target) {
            j--;
        } else {
            if (a[i] == a[j]) {
                long long m = j - i + 1;
                count += m * (m - 1) / 2;
                break;
            }
            long long leftCount = 1;
            while (i + leftCount < j && a[i + leftCount] == a[i]) leftCount++;
            long long rightCount = 1;
            while (j - rightCount > i && a[j - rightCount] == a[j]) rightCount++;
            count += leftCount * rightCount;
            i += leftCount;
            j -= rightCount;
        }
    }
    return count;
}
