# Maximum Subarray Sum with Updates

You are given an integer sequence $a_1, a_2, \dots, a_n$. Then $q$ operations follow, each of one of two kinds:

- `1 x v`: set the $x$-th number to $v$, i.e. $a_x \leftarrow v$;
- `2 l r`: ask for the **maximum subarray sum** of the segment $[l, r]$:

$$\max_{l \le i \le j \le r} \sum_{k=i}^{j} a_k.$$

The subarray must be non-empty (that is, $i \le j$). Apply all operations in order and answer every query in order.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains three integers describing one operation:

- `1 x v` is a point assignment;
- `2 l r` is a maximum-subarray query.

It is guaranteed that there is at least one operation of type `2`.

### Output

One line with the answers of all queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le n \le 5 \times 10^4$
- $1 \le q \le 10^5$
- $1 \le x, l \le r \le n$
- $-10^9 \le a_i, v \le 10^9$
- The absolute value of every segment sum is at most $2 \times 10^{14}$

### Sample explanation

The initial sequence is $1, -2, 3, -1, 2$.

The first operation `2 1 5` asks for the maximum subarray sum of the whole array; taking $[3, 5]$ gives $3 + (-1) + 2 = 4$.

The second operation `1 2 3` sets the second number to $3$, so the array becomes $1, 3, 3, -1, 2$.

The third operation `2 1 5` asks for the whole array again; taking $[1, 5]$ gives $1 + 3 + 3 + (-1) + 2 = 8$.

The fourth operation `2 2 2` asks for the single-element segment $[2, 2]$, so the answer is $3$.

Hence the output is `4 8 3`.
