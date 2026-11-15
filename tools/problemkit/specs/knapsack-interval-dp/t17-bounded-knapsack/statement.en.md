# Bounded Knapsack Maximum Value

There are $n$ kinds of items and a knapsack of capacity $cap$. The $i$-th kind of item has weight $w_i$, value $v_i$ and there are $c_i$ copies of it. Find the maximum total value of a multiset of items whose total weight does not exceed $cap$.

### Input

- The first line contains two integers $n$ and $cap$, separated by a single space.
- The second line contains $n$ integers $w_1, w_2, \dots, w_n$.
- The third line contains $n$ integers $v_1, v_2, \dots, v_n$.
- The fourth line contains $n$ integers $c_1, c_2, \dots, c_n$.

Consecutive integers are separated by single spaces.

### Output

One integer: the maximum total value.

### Constraints

$1 \le n \le 100$, $1 \le cap \le 1000$, $1 \le w_i \le cap$, $0 \le v_i \le 10^{9}$, $1 \le c_i \le 10^{9}$.

Note that $c_i$ may be huge, so expanding each kind into $c_i$ single items is too slow. The answer does not exceed $10^{12}$.

### Sample explanation

Sample 1: $n = 2$, $cap = 10$. Kind $1$ has weight $3$, value $4$, $3$ copies; kind $2$ has weight $5$, value $7$, $2$ copies. Taking two copies of kind $2$ uses weight $10$ and gives value $14$, which is optimal.
