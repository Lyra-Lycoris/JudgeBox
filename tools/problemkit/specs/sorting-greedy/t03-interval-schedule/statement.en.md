# Interval Scheduling: Maximum Non-overlapping Intervals

There are $n$ closed intervals on the number line; the $i$-th one is $[l_i, r_i]$. Choose as many intervals as possible so that no two chosen intervals overlap. Two intervals $[l, r]$ and $[l', r']$ are considered non-overlapping only when $r \le l'$ (touching endpoints are allowed).

Output the maximum number of intervals you can choose.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $l_1, l_2, \dots, l_n$.

The third line contains $n$ integers $r_1, r_2, \dots, r_n$.

It is guaranteed that $l_i \le r_i$.

### Output

One integer: the maximum number of intervals that can be chosen.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $-10^9 \le l_i \le r_i \le 10^9$

### Sample explanation

The sample has four intervals: $[1,3]$, $[2,4]$, $[3,5]$ and $[0,1]$. Sorting them by right endpoint gives $[0,1], [1,3], [2,4], [3,5]$; taking $[0,1]$, $[1,3]$ and $[3,5]$ yields three pairwise non-overlapping intervals. Four is impossible, so the answer is 3.
