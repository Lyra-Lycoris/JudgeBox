# Grouped Knapsack: At Most One per Group

There are $n$ items and a knapsack of capacity $cap$. Item $i$ belongs to group $g_i$, has weight $w_i$ and value $v_i$. At most one item may be taken from each group (a group may also contribute nothing). Find the maximum total value of a valid selection whose total weight does not exceed $cap$.

### Input

- The first line contains two integers $n$ and $cap$, separated by a single space.
- The second line contains $n$ integers $g_1, g_2, \dots, g_n$: the group of each item.
- The third line contains $n$ integers $w_1, w_2, \dots, w_n$.
- The fourth line contains $n$ integers $v_1, v_2, \dots, v_n$.

Consecutive integers are separated by single spaces. Items with equal $g_i$ belong to the same group.

### Output

One integer: the maximum total value.

### Constraints

$1 \le n \le 300$, $1 \le cap \le 2000$, $1 \le g_i \le n$, $1 \le w_i \le 10^{9}$, $0 \le v_i \le 10^{9}$.

An item heavier than $cap$ can never be selected. The answer does not exceed $10^{12}$.

### Sample explanation

Sample 1: $n = 3$, $cap = 15$, items $(g, w, v) = (1, 5, 10), (1, 6, 11), (2, 7, 20)$. Group $1$ allows one item, so take the second one (weight $6$, value $11$); group $2$ has a single item (weight $7$, value $20$). The total weight is $13 \le 15$ and the total value is $31$, which is optimal.
