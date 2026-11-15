# Square-Root Decomposition: Range Add and Range Maximum

You are given an integer array $a_1, a_2, \dots, a_n$ of length $n$ and $q$ operations. Each operation is of one of two kinds:

- `1 l r x`: add $x$ to every element in $[l, r]$;
- `2 l r 0`: output the range maximum $\max_{l \le i \le r} a_i$.

Apply all operations in order and answer every query in order.

So that every line contains the same number of integers, both kinds of operations supply $4$ integers: for a query the last one is always $0$ and is ignored.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains four integers $t, l, r, x$:

- $t = 1$ means add $x$ to every element of $[l, r]$;
- $t = 2$ means ask for the maximum of $[l, r]$; in this case $x$ is always $0$.

There is at least one operation with $t = 2$.

### Output

One line with the answers of all queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le n \le 2 \times 10^5$, $1 \le q \le 2 \times 10^4$
- $1 \le l \le r \le n$
- $|a_i| \le 10^6$, $|x| \le 10^6$

### Sample explanation

Initially the array is $1, 3, -2, 4, 5$.

`2 1 5 0` asks for the maximum of the whole array, which is $5$.

`1 2 4 10` adds $10$ to elements $2 \sim 4$, giving $1, 13, 8, 14, 5$.

`2 1 5 0` asks for the maximum of the whole array, which is $14$.

`2 2 3 0` asks for the maximum of $[2, 3]$, which is $\max(13, 8) = 13$.

`1 1 5 -20` subtracts $20$ from every element, giving $-19, -7, -12, -6, -15$.

`2 1 5 0` asks for the maximum of the whole array, which is $-6$.

Hence the output is `5 14 13 -6`.
