# Range Add and Point Query

You are given an integer sequence $a_1, a_2, \dots, a_n$. Then $q$ operations follow; each operation is described by four integers $t, l, r, v$:

- $t = 1$: add $v$ to every element of $[l, r]$, i.e. $a_i \leftarrow a_i + v\ (l \le i \le r)$;
- $t = 2$: ask for the current value of $a_l$. In this case $r = 0$ and $v = 0$ are guaranteed (they are not used).

Apply all operations in order and answer every point query in order.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains four integers $t, l, r, v$ describing one operation. There is at least one operation with $t = 2$.

### Output

One line with the answers of all queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le q \le 10^5$
- $1 \le l \le r \le n$ (when $t = 1$), $1 \le l \le n$ (when $t = 2$)
- $-10^9 \le a_i, v \le 10^9$
- Every element always stays inside $[-2 \times 10^{14}, 2 \times 10^{14}]$

### Sample explanation

The initial sequence is $1, 2, 3, 4, 5$.

The first operation `1 1 3 10` adds $10$ to $[1, 3]$, so the sequence becomes $11, 12, 13, 4, 5$.

The second operation `2 2 0 0` asks for the second number, which is $12$.

The third operation `1 2 5 -4` adds $-4$ to $[2, 5]$, so the sequence becomes $11, 8, 9, 0, 1$.

The fourth operation `2 3 0 0` asks for the third number, which is $9$.

Hence the output is `12 9`.
