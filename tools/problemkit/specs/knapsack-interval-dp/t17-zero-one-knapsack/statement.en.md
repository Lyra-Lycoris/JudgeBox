# 0/1 Knapsack Maximum Value

There are $n$ items and a knapsack of capacity $cap$. Item $i$ has weight $w_i$ and value $v_i$, and each item may be chosen at most once. Find the maximum total value of a subset of items whose total weight does not exceed $cap$.

### Input

- The first line contains two integers $n$ and $cap$, separated by a single space.
- The second line contains $n$ integers $w_1, w_2, \dots, w_n$, separated by single spaces.
- The third line contains $n$ integers $v_1, v_2, \dots, v_n$, separated by single spaces.

### Output

One integer: the maximum total value.

### Constraints

$1 \le n \le 1000$, $1 \le cap \le 2000$, $1 \le w_i \le 10^{9}$, $0 \le v_i \le 10^{9}$.

An item heavier than $cap$ can never be selected. The answer does not exceed $10^{12}$.

### Sample explanation

Sample 1: $n = 3$, $cap = 10$, weights $(5, 4, 6)$, values $(10, 40, 30)$. Taking items $2$ and $3$ uses weight $4 + 6 = 10$ and gives value $40 + 30 = 70$, which is optimal.
