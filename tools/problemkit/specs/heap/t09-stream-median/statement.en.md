# Streaming Median

An integer stream arrives one value at a time. Definition: after the $i$-th value has been inserted, the **median** of the current stream is the $\lceil i / 2 \rceil$-th smallest value among those $i$ values (so for even $i$ it is the smaller of the two middle values).

You are given $T$ test cases. For each case, insert its values one by one and print the median after every insertion.

### Input

The first line contains an integer $T$: the number of test cases.

Each case consists of two lines:

- one integer $n$;
- $n$ integers in arrival order.

### Output

For each case print one line with $n$ integers: the medians after inserting the $1$-st, $2$-nd, $\dots$, $n$-th value, separated by spaces.

### Constraints

- $1 \le T \le 10$
- $1 \le n \le 200000$, and the sum of all $n$ over the test cases is at most $200000$
- $|a_i| \le 10^9$

### Sample Explanation

For $[1,2,3]$ the medians are $1, 1, 2$; for $[5,4,3,2]$ the medians are $5, 4, 4, 3$.
