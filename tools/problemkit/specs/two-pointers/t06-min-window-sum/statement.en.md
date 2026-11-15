# Shortest Subarray with Sum at Least S

Given $n$ **positive** integers $a_1, a_2, \dots, a_n$ and an integer $S$, find a contiguous subarray whose elements sum to at least $S$ and whose length is as small as possible. Print that minimum length, or `0` when no such subarray exists.

### Input

The first line contains two integers $n$ and $S$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$ separated by single spaces.

### Output

One integer: the minimum length of a contiguous subarray with sum at least $S$, or `0` if there is none.

### Constraints

- $1 \le n \le 200000$
- $1 \le a_i \le 10^9$
- $1 \le S \le 10^{14}$

### Sample explanation

Sample 1: $n = 6$, $S = 7$, array $2, 3, 1, 2, 4, 3$. The subarray $[4, 3]$ has sum $7$ and length $2$, and no single element reaches $7$, so the answer is $2$.

Sample 2: $n = 1$, $S = 6$, the only element is $5$, which is too small, so the answer is `0`.

Sample 3: the whole array sums to $5$, far below $S = 100$, so the answer is `0`.
