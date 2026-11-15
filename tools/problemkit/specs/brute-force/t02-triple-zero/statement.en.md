# Counting Zero-Sum Triples

Given an integer sequence $a_1, a_2, \dots, a_n$ of length $n$, count the number of index triples $(i, j, k)$ such that

- $1 \le i < j < k \le n$;
- $a_i + a_j + a_k = 0$.

The indices must be strictly increasing, so equal values at different positions are counted separately.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by spaces.

### Output

Print a single integer: the number of valid triples.

### Constraints

- $1 \le n \le 300$
- $-10^9 \le a_i \le 10^9$
- The answer does not exceed $10^{18}$; use a 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
3
-1 0 1
```

**Output**

```
1
```

### Sample explanation

Here $a = \{-1, 0, 1\}$ and the only triple with sum $0$ is $(-1, 0, 1)$, so the output is `1`.

For the input `3` followed by `0 0 0`, the triple $(1, 2, 3)$ also sums to $0$, so the output is `1` as well.
