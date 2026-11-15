# Count Distinct in Range

You are given an integer sequence $a_1, a_2, \dots, a_n$.

Then $q$ queries follow; the $j$-th query gives $l_j, r_j$ and asks: how many **distinct** values appear among $a_{l_j}, a_{l_j+1}, \dots, a_{r_j}$?

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains two integers $l_j, r_j$.

### Output

One line with the answers of all queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le q \le 10^5$
- $1 \le l_j \le r_j \le n$
- $-10^9 \le a_i \le 10^9$

### Sample explanation

The sequence is $1, 2, 1, 3, 2, 1$.

- Query $[1, 6]$: the values $1, 2, 3$ appear, so the answer is $3$;
- Query $[1, 3]$: the values $1, 2$ appear, so the answer is $2$;
- Query $[2, 4]$: the values $2, 1, 3$ appear, so the answer is $3$;
- Query $[4, 4]$: only $3$ appears, so the answer is $1$.

Hence the output is `3 2 3 1`.
