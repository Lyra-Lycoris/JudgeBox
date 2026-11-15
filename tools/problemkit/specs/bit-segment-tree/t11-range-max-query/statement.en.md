# Static Range Maximum Query

You are given an integer sequence $a_1, a_2, \dots, a_n$. The sequence **never changes** during the queries.

Then $q$ queries follow; the $j$-th query gives $l_j, r_j$ and asks for

$$\max_{l_j \le i \le r_j} a_i.$$

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains two integers $l_j, r_j$.

### Output

One line with the answers of all queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le q \le 2 \times 10^5$
- $1 \le l_j \le r_j \le n$
- $-10^9 \le a_i \le 10^9$

### Sample explanation

The sequence is $1, 7, 3, 9, 2, 8$.

- Query $[1, 3]$: the maximum is $\max(1, 7, 3) = 7$;
- Query $[4, 6]$: the maximum is $\max(9, 2, 8) = 9$;
- Query $[2, 2]$: a single element, so the answer is $7$;
- Query $[1, 6]$: the maximum is $9$.

Hence the output is `7 9 7 9`.
