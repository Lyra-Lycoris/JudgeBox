# Counting Subarrays with At Least k Inversions

Given a sequence of $n$ integers $a_1, a_2, \dots, a_n$ and a non-negative integer $k$.

For a contiguous subarray $[l, r]$ ($1 \le l \le r \le n$), its **inversion count** is the number of index pairs $(i, j)$ such that

$$l \le i < j \le r \quad\text{and}\quad a_i > a_j.$$

Count how many contiguous subarrays have an inversion count of at least $k$.

### Input

- The first line contains two integers $n$ and $k$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

A single integer: the number of contiguous subarrays with at least $k$ inversions.

### Constraints

- $1 \le n \le 100000$
- $0 \le k \le 10^{10}$
- $|a_i| \le 10^9$

There are at most $\frac{n(n+1)}{2} = 5000050000$ subarrays, so the answer fits in a 64-bit integer.

### Sample explanation

Sample 1: $n = 3$, $k = 1$, sequence $2, 1, 3$. The subarrays $[2]$, $[1]$, $[3]$ and $[1, 3]$ have $0$ inversions, while $[2, 1]$ and $[2, 1, 3]$ have $1$ inversion each. Two subarrays have at least $1$ inversion, so the output is `2`.

Sample 2: $n = 3$, $k = 0$, sequence $5, 5, 5$. Every subarray has $0 \ge 0$ inversions, so all $\frac{3 \times 4}{2} = 6$ subarrays qualify; the output is `6`.

Sample 3: $n = 3$, $k = 2$, sequence $3, 2, 1$. The six subarrays have $0, 0, 0, 1, 1, 3$ inversions respectively, and only the whole sequence reaches $2$, so the output is `1`.

### Hint

For a fixed left endpoint $l$, the inversion count does not decrease as the right endpoint $r$ grows; for a fixed $r$, it does not increase as $l$ grows. Therefore the smallest $r$ such that $[l, r]$ has at least $k$ inversions is itself non-decreasing in $l$, so a two-pointer sliding window works.

Maintaining the window's inversion count requires adding and removing elements:

- adding $x$ creates one new inversion for every element in the window strictly greater than $x$;
- removing $x$ destroys one inversion for every element in the window strictly smaller than $x$.

Keep the frequencies of the window elements in a Fenwick tree (or a balanced tree) so that each update costs $O(\log n)$. The pointers move $O(n)$ times in total, giving $O(n \log n)$ overall.
