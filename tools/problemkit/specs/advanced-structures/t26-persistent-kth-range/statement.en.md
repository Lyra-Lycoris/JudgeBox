# Static Range K-th Smallest

You are given an integer array $a_1, a_2, \dots, a_n$ of length $n$ and $m$ queries. Each query gives $l, r, k$; output the $k$-th smallest value in the subarray $a_l, a_{l+1}, \dots, a_r$ (equal values are counted with their multiplicity).

A possible approach is a **persistent segment tree**: compress the values of the array, insert the positions one by one in prefix order, so that version $i$ stores the value-domain counts of $a_1 \dots a_i$. For a query $[l, r]$, subtract version $l-1$ from version $r$ and walk down the value-domain tree for $O(\log n)$ steps to locate the $k$-th smallest value. A merge sort tree with binary search also works.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $m$.

Each of the next $m$ lines contains three integers $l, r, k$, describing one query.

### Output

One line with the answers of all queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le n, m \le 5 \times 10^4$
- $1 \le l \le r \le n$
- $1 \le k \le r - l + 1$
- $|a_i| \le 10^9$

### Sample explanation

The array is $3, 1, 4, 1, 5$ and there are $3$ queries.

- $[1, 5]$ sorted is $1, 1, 3, 4, 5$, so the $1$-st smallest is $1$;
- $[3, 5]$ sorted is $1, 4, 5$, so the $2$-nd smallest is $4$;
- $[2, 4]$ sorted is $1, 1, 4$, so the $2$-nd smallest is $1$.

Hence the output is `1 4 1`.
