# Range Mode Query (Square-Root Decomposition)

You are given an integer array $a_1, a_2, \dots, a_n$ of length $n$ and $q$ queries. Each query gives two integers $l, r$; you have to find the **mode** of the subarray $a_l, a_{l+1}, \dots, a_r$, i.e. the value that occurs most often.

If several values occur equally often and are tied for the maximum, output the **smallest** of them.

One possible approach is square-root decomposition: split the array into blocks of size about $\sqrt n$, precompute the mode of every range made of whole blocks, and for a query start from that answer, then brute-force the two incomplete boundary blocks and count occurrences with binary search over the sorted list of positions of each value. This gives $O(n\sqrt n)$ preprocessing and $O(\sqrt n \log n)$ per query.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains two integers $l, r$, describing one query.

### Output

One line with the mode of every query in the order the queries appear, separated by single spaces.

### Constraints

- $1 \le n, q \le 5 \times 10^4$
- $1 \le l \le r \le n$
- $|a_i| \le 10^9$

### Sample explanation

The array is $1, 2, 2, 3, 1, 3$ and there are $4$ queries.

- $[1, 6]$: the values $1, 2, 3$ all occur twice, so the smallest one, $1$, is the answer;
- $[2, 3]$: only $2, 2$, so the answer is $2$;
- $[1, 3]$: $1$ occurs once and $2$ occurs twice, so the answer is $2$;
- $[4, 6]$: $3$ occurs twice and $1$ occurs once, so the answer is $3$.

Hence the output is `1 2 2 3`.
