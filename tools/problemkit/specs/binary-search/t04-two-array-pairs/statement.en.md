# Pairs with Sum at Most x

You are given two integer arrays $a_0, a_1, \dots, a_{n-1}$ and $b_0, b_1, \dots, b_{m-1}$, and an integer $x$.

Count the number of index pairs $(i, j)$ with $a_i + b_j \le x$, where $0 \le i < n$ and $0 \le j < m$.

Index pairs are ordered (a pair $(i, j)$ and a pair $(j, i)$ are different, since the two arrays are different), and the same index may appear in many pairs.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_0, a_1, \dots, a_{n-1}$.

The third line contains one integer $m$.

The fourth line contains $m$ integers $b_0, b_1, \dots, b_{m-1}$.

The fifth line contains one integer $x$.

### Output

One integer: the number of pairs with $a_i + b_j \le x$.

### Constraints

- $1 \le n, m \le 2 \times 10^5$
- $-10^9 \le a_i, b_j \le 10^9$
- $-2 \times 10^9 \le x \le 2 \times 10^9$
- The answer is at most $n \times m \le 4 \times 10^{10}$, which fits in a 64-bit integer

### Sample explanation

With $n = 3$, $a = [1, 2, 3]$; $m = 3$, $b = [4, 5, 6]$; and $x = 7$:

- $a_0 = 1$: $1 + 4 = 5$, $1 + 5 = 6$ and $1 + 6 = 7$ all qualify, that is $3$ pairs.
- $a_1 = 2$: $2 + 4 = 6$ and $2 + 5 = 7$ qualify, $2 + 6 = 8$ does not, that is $2$ pairs.
- $a_2 = 3$: only $3 + 4 = 7$ qualifies, that is $1$ pair.

The total is $3 + 2 + 1 = 6$, so the answer is $6$.

Approach: sort $b$, then for every $a_i$ use binary search to count how many elements of $b$ are at most $x - a_i$. The total complexity is $O(n \log m)$.
