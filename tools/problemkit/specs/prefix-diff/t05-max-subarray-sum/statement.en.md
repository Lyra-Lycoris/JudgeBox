# Maximum Subarray Sum

You are given an integer sequence $a_1, a_2, \dots, a_n$. Find a **non-empty** contiguous segment $a_l, a_{l+1}, \dots, a_r$ ($1 \le l \le r \le n$) with the largest possible sum and output that maximum sum.

Let $P_0 = 0$ and $P_i = a_1 + a_2 + \dots + a_i$. A segment sum equals $P_r - P_{l-1}$, so the task is to maximize $P_r - P_{l-1}$ over $l-1 < r$.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

### Output

One integer: the maximum segment sum.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $-10^9 \le a_i \le 10^9$
- The absolute value of the answer does not exceed $2 \times 10^{14}$

### Sample explanation

The sequence is $-2, 1, -3, 4, -1, 2, 1, -5$. Taking the segment $4, -1, 2, 1$ (elements $4$ through $7$) gives sum $6$, which is the largest sum of any non-empty contiguous segment.
