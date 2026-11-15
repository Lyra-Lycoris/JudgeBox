# K Smallest Pair Sums

Given two **non-decreasing** integer sequences $a_1 \le a_2 \le \dots \le a_n$ and $b_1 \le b_2 \le \dots \le b_m$, consider the $n \times m$ sums $a_i + b_j$ over all index pairs $(i, j)$. Output the smallest $k$ of these sums in non-decreasing order (equal sums are counted separately).

### Input

The first line contains three integers $n$, $m$ and $k$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$ (non-decreasing).

The third line contains $m$ integers $b_1, b_2, \dots, b_m$ (non-decreasing).

### Output

One line with the $k$ smallest sums in non-decreasing order, separated by spaces.

### Constraints

- $1 \le n, m \le 100000$
- $1 \le k \le \min(n \times m,\ 100000)$
- $|a_i|, |b_j| \le 10^9$
- Both sequences are guaranteed to be non-decreasing

### Sample Explanation

$a = [1, 7, 11]$ and $b = [2, 4, 6]$. The smallest sums are $1+2=3$, $1+4=5$, $1+6=7$ and $7+2=9$, so for $k=3$ the answer is `3 5 7`.
