# Maximize the Minimum Adjacent Difference

Given $n$ integers $a_1, a_2, \dots, a_n$, choose exactly $k$ of them. Sort the chosen values increasingly and let $D$ be the minimum difference between adjacent values ($D = 0$ when $k = 1$). Compute the maximum possible value of $D$.

The chosen elements need not be contiguous in the original array; you may pick any $k$ of them.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $k$.

### Output

One integer: the maximum possible value of $D$.

### Constraints

- $1 \le k \le n \le 10^5$
- $|a_i| \le 10^9$

### Sample explanation

With $n = 5$, array $1, 5, 3, 9, 11$ and $k = 3$, the sorted array is $1, 3, 5, 9, 11$. Choosing $1, 5, 9$ gives adjacent differences $4$ and $4$, so $D = 4$.

For $D \ge 5$: after choosing $1$ the next chosen value must be at least $6$, which forces $9$; the value after that must be at least $14$, which does not exist, so at most $2$ values can be chosen. Hence $D$ cannot exceed $4$ and the answer is $4$.
