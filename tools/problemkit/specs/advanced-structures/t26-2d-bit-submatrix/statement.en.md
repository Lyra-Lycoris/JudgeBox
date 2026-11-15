# 2D Fenwick Tree: Point Update and Submatrix Sum

You are given an integer matrix $A$ with $n$ rows and $m$ columns (both rows and columns are numbered from $1$), and $q$ operations. Each operation is of one of two kinds:

- `1 x y v 0`: increase $A_{x,y}$ by $v$;
- `2 x1 y1 x2 y2`: output the sum of the submatrix
$$\sum_{i=x_1}^{x_2}\sum_{j=y_1}^{y_2} A_{i,j}.$$

Apply all operations in order and answer every query in order.

So that every line contains the same number of integers, both kinds of operations supply $5$ integers: for an update the last one is always $0$ and is ignored.

### Input

The first line contains two integers $n, m$.

Each of the next $n$ lines contains $m$ integers describing the matrix $A$.

The next line contains one integer $q$.

Each of the next $q$ lines contains five integers $t, a, b, c, d$:

- $t = 1$ is an update: $a = x$, $b = y$, $c = v$, $d$ is always $0$, meaning $A_{x,y} \leftarrow A_{x,y} + v$;
- $t = 2$ is a query: $a = x_1$, $b = y_1$, $c = x_2$, $d = y_2$.

There is at least one operation with $t = 2$.

### Output

One line with the answers of all queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le n, m \le 500$, $1 \le q \le 3 \times 10^4$
- $|A_{i,j}| \le 10^6$, $|v| \le 10^6$
- $1 \le x \le n$, $1 \le y \le m$
- $1 \le x_1 \le x_2 \le n$, $1 \le y_1 \le y_2 \le m$
- The absolute value of every answer does not exceed $10^{12}$

### Sample explanation

The matrix is

$$A = \begin{pmatrix} 1 & 2 & 3 & 4 \\ 5 & 6 & 7 & 8 \\ 9 & 10 & 11 & 12 \end{pmatrix}$$

`2 1 1 2 2` asks for the top-left $2 \times 2$ submatrix: $1 + 2 + 5 + 6 = 14$.

`1 2 2 100 0` increases $A_{2,2}$ by $100$, so it changes from $6$ to $106$.

`2 1 1 2 2` asks for the same submatrix again: $1 + 2 + 5 + 106 = 114$.

`2 2 2 3 4` asks for rows $2 \sim 3$ and columns $2 \sim 4$: $106 + 7 + 8 + 10 + 11 + 12 = 154$.

Hence the output is `14 114 154`.
