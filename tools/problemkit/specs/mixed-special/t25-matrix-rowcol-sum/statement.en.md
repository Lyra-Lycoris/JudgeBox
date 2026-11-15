# Construct a Matrix with Given Row and Column Sums

You are given $n$, $m$, a row-sum array $r_1, \dots, r_n$ of length $n$ and a column-sum array $c_1, \dots, c_m$ of length $m$ (it is guaranteed that $\sum r_i = \sum c_j$).

Construct an $n \times m$ matrix $A$ of **non-negative integers** such that:

- the sum of all elements in row $i$ equals $r_i$;
- the sum of all elements in column $j$ equals $c_j$.

This problem uses a **special judge** (SPJ): any valid matrix is accepted.

### Input

- The first line contains two integers $n$ and $m$.
- The second line contains $n$ integers $r_1, \dots, r_n$.
- The third line contains $m$ integers $c_1, \dots, c_m$.

### Output

Print the $n \times m$ non-negative integers in **row-major** order: first the $m$ numbers of row $1$, then the $m$ numbers of row $2$, and so on. The numbers may be separated by spaces or newlines, but you must print exactly $n \times m$ numbers.

### Constraints

$1 \le n, m \le 100$, $0 \le r_i, c_j \le 10^9$ and $\sum r_i = \sum c_j$. A solution always exists.

### Sample explanation

Sample 1: $n = 2$, $m = 3$, $r = (3, 3)$, $c = (2, 2, 2)$. The output `2 1 0 0 1 2` corresponds to the matrix

$$\begin{pmatrix} 2 & 1 & 0 \\ 0 & 1 & 2 \end{pmatrix}$$

whose row sums are $3, 3$ and whose column sums are $2, 2, 2$, so every requirement is met.

### Hint

Fill the cells in row-major order. At cell $(i, j)$ write $\min(r_i, c_j)$, then subtract that value from both $r_i$ and $c_j$. When a row is finished its remaining row sum is exactly zero, and the same holds for every column, so the constructed matrix always satisfies the requirements (all entries stay non-negative).
