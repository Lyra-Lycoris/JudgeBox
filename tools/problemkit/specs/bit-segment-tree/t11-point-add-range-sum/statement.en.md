# Point Add and Range Sum

You are given an integer sequence $a_1, a_2, \dots, a_n$. Then $q$ operations follow, each of one of two kinds:

- `1 x v`: increase the $x$-th number by $v$, i.e. $a_x \leftarrow a_x + v$;
- `2 l r`: ask for the sum of the segment $[l, r]$, i.e. $\sum_{i=l}^{r} a_i$.

Apply all operations in order and answer every query in order.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains three integers describing one operation:

- `1 x v` is a point add;
- `2 l r` is a range-sum query.

It is guaranteed that there is at least one operation of type `2`.

### Output

One line with the answers of all queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le q \le 10^5$
- $1 \le x, l \le r \le n$
- $-10^9 \le a_i, v \le 10^9$
- The total sum of the sequence always stays inside $[-2 \times 10^{14}, 2 \times 10^{14}]$

### Sample explanation

The initial sequence is $1, 2, 3, 4, 5$.

The first operation `1 3 10` adds $10$ to the third number, so the sequence becomes $1, 2, 13, 4, 5$.

The second operation `2 1 3` asks for the sum of $[1, 3]$, which is $1 + 2 + 13 = 16$.

The third operation `2 2 5` asks for the sum of $[2, 5]$, which is $2 + 13 + 4 + 5 = 24$.

Hence the output is `16 24`.
