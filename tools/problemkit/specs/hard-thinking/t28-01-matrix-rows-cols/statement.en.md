# 0/1 Matrix with Given Row and Column Sums

You are given $n$, $m$, an array $r_1, \dots, r_n$ of length $n$ and an array $c_1, \dots, c_m$ of length $m$.

Construct an $n \times m$ matrix $A$ such that:

- every entry of $A$ is either $0$ or $1$;
- the sum of row $i$ equals $r_i$ for every $1 \le i \le n$;
- the sum of column $j$ equals $c_j$ for every $1 \le j \le m$.

It is guaranteed that at least one such matrix exists.

This problem uses a **special judge** (SPJ): any valid matrix is accepted, it does not have to match the reference answer.

### Input

- The first line contains two integers $n$ and $m$.
- The second line contains $n$ integers $r_1, \dots, r_n$.
- The third line contains $m$ integers $c_1, \dots, c_m$.

### Output

Print the $n \times m$ entries in **row-major** order: first the $m$ numbers of row $1$, then the $m$ numbers of row $2$, and so on. Entries may be separated by spaces or newlines, but there must be exactly $n \times m$ numbers, each of them $0$ or $1$.

### Constraints

- $1 \le n, m \le 300$
- $0 \le r_i \le m$ and $0 \le c_j \le n$
- $\sum_{i=1}^{n} r_i = \sum_{j=1}^{m} c_j$
- At least one valid $0/1$ matrix exists

### Sample explanation

For $n = 3$, $m = 4$, $r = (2, 1, 1)$ and $c = (1, 1, 1, 1)$ the output

```
1 1 0 0
0 0 1 0
0 0 0 1
```

is the matrix

$$\begin{pmatrix} 1 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix},$$

whose row sums are $2, 1, 1$ and column sums are $1, 1, 1, 1$. The answer is not unique; for example

$$\begin{pmatrix} 0 & 1 & 1 & 0 \\ 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

is accepted as well.

### Hint

Entries must be $0$ or $1$, so one cannot simply fill $\min(r_i, c_j)$ as for non-negative integer matrices; every cell has to stay within $1$.

A correct greedy is: sort all rows by $r_i$ **in decreasing order** (ties broken by the original row index) and process them one by one. For the current row, put a $1$ into the $r_i$ columns with the **largest remaining column sums** (ties broken arbitrarily, e.g. by the smaller column index), then decrease those remaining sums by one.

Correctness follows from an exchange argument (it is the constructive form of the Gale–Ryser theorem): if in some valid matrix the row with the largest demand does not use the columns with the largest remaining sums, we can always swap two entries between columns and reach the greedy shape without violating any constraint. Hence the greedy never makes a remaining column sum negative and never gets stuck.

For an easy implementation, replace a balanced structure by "encode and sort": encode the remaining sum $s_j$ of column $j$ as $s_j \cdot B + (B - 1 - j)$ with a constant $B > \max(n, m)$. Sorting these values and taking the last $r_i$ of them gives exactly "column sum decreasing, column index increasing". The total complexity is $O(n m \log m)$.
