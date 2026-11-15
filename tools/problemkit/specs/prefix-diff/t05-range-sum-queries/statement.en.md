# Range Sum Queries

You are given an integer sequence $a_1, a_2, \dots, a_n$. There are $T$ independent test cases. Each case also gives a query segment $[l, r]$; answer

$$\sum_{i=l}^{r} a_i = a_l + a_{l+1} + \dots + a_r.$$

### Input

The first line contains one integer $T$, the number of test cases.

For each test case, the following lines are given in order:

- one integer $n$, the length of the sequence;
- $n$ integers $a_1, a_2, \dots, a_n$;
- two integers $l, r$, the query segment.

### Output

Output $T$ lines; for each test case print one integer, the sum over its query segment.

### Constraints

- $1 \le T \le 5$
- For each case $1 \le n \le 2 \times 10^5$, and the sum of $n$ over all cases of one input does not exceed $2 \times 10^5$
- $-10^9 \le a_i \le 10^9$
- $1 \le l \le r \le n$

### Sample explanation

In the first case the sequence is $1, 2, 3$ and the query is $[1, 3]$, so the sum is $1+2+3=6$.

In the second case the sequence is $-1, 5, -2, 4$ and the query is $[2, 3]$, so the sum is $5 + (-2) = 3$.
