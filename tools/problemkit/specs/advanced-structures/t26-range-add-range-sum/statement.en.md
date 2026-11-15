# Range Add and Range Sum (Twin Fenwick Trees)

You are given an integer array $a_1, a_2, \dots, a_n$ of length $n$ and $q$ operations. Each operation is of one of two kinds:

- `1 l r x`: add $x$ to every element in $[l, r]$, i.e. $a_i \leftarrow a_i + x$ for all $l \le i \le r$;
- `2 l r 0`: output the range sum $\sum_{i=l}^{r} a_i$.

Apply all operations in order and answer every operation of the second kind in order.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains four integers $t, l, r, x$:

- $t = 1$ means add $x$ to every element of $[l, r]$;
- $t = 2$ means ask for the sum of $[l, r]$; in this case the fourth integer is always $0$ and is ignored.

There is at least one operation with $t = 2$.

### Output

One line with the answers of all range-sum queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le n \le 2 \times 10^5$, $1 \le q \le 10^5$
- $1 \le l \le r \le n$
- $|a_i| \le 10^6$, $|x| \le 10^6$
- At any moment $\sum_{i=1}^{n} |a_i| \le 10^{15}$, so every answer fits in a 64-bit integer

### Sample explanation

Initially the array is $1, 2, 3, 4, 5$.

`1 1 3 10` adds $10$ to the first three elements, giving $11, 12, 13, 4, 5$.

`2 1 5 0` asks for the sum of the whole array: $11 + 12 + 13 + 4 + 5 = 45$.

`1 2 2 -5` subtracts $5$ from the second element, giving $11, 7, 13, 4, 5$.

`2 2 4 0` asks for the sum of $[2, 4]$: $7 + 13 + 4 = 24$.

Hence the output is `45 24`.
