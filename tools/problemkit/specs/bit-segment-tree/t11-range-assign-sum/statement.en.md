# Range Assign and Total Sum

You are given an integer sequence $a_1, a_2, \dots, a_n$. Then $q$ operations follow; the $j$-th operation gives three integers $l_j, r_j, v_j$ and sets **every** element of $[l_j, r_j]$ to $v_j$:

$$a_i \leftarrow v_j \quad (l_j \le i \le r_j).$$

After each operation, output the total sum of the whole sequence, $\sum_{i=1}^{n} a_i$.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains three integers $l_j, r_j, v_j$, describing one range-assign operation.

### Output

One line with $q$ integers; the $j$-th one is the total sum right after the $j$-th operation, separated by single spaces.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le q \le 10^5$
- $1 \le l_j \le r_j \le n$
- $-10^9 \le a_i, v_j \le 10^9$
- The total sum always stays inside $[-2 \times 10^{14}, 2 \times 10^{14}]$

### Sample explanation

The initial sequence is $1, 2, 3, 4, 5$.

The first operation `1 3 7` sets $[1, 3]$ to $7$, so the sequence becomes $7, 7, 7, 4, 5$ and the total sum is $30$.

The second operation `2 5 0` sets $[2, 5]$ to $0$, so the sequence becomes $7, 0, 0, 0, 0$ and the total sum is $7$.

The third operation `1 5 2` sets $[1, 5]$ to $2$, so the sequence becomes $2, 2, 2, 2, 2$ and the total sum is $10$.

Hence the output is `30 7 10`.
