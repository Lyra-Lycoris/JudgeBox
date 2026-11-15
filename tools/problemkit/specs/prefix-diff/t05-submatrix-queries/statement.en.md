# Submatrix Sum Queries

You are given an $n \times m$ integer matrix $g$ whose row and column indices start from $1$. There are $q$ queries; the $t$-th query gives $x_1, y_1, x_2, y_2$ and asks for the sum of all elements of the submatrix with top-left corner $(x_1, y_1)$ and bottom-right corner $(x_2, y_2)$:

$$\sum_{i=x_1}^{x_2} \sum_{j=y_1}^{y_2} g_{i,j}.$$

### Input

The first line contains two integers $n, m$.

Each of the next $n$ lines contains $m$ integers describing the matrix $g$.

The next line contains one integer $q$.

Each of the next $q$ lines contains four integers $x_1, y_1, x_2, y_2$ describing one query. It is guaranteed that $1 \le x_1 \le x_2 \le n$ and $1 \le y_1 \le y_2 \le m$.

### Output

One line with $q$ integers separated by spaces; the $t$-th number is the answer to the $t$-th query.

### Constraints

- $1 \le n, m \le 500$
- $1 \le q \le 10^5$
- $-10^9 \le g_{i,j} \le 10^9$
- The absolute value of the sum of any single submatrix does not exceed $2.5 \times 10^{14}$

### Sample explanation

The matrix is

$$\begin{pmatrix} 1 & 2 & 3 & 4 \\ 5 & 6 & 7 & 8 \\ 9 & 10 & 11 & 12 \end{pmatrix}.$$

The first query takes the whole matrix, whose sum is $78$.

The second query takes rows $2$ to $3$ and columns $2$ to $3$, namely $6, 7, 10, 11$, whose sum is $34$.
