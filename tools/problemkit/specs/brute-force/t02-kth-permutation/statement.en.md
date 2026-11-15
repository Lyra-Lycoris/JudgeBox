# The k-th Permutation

Given an integer $n$, sort all permutations of $1, 2, \dots, n$ in lexicographic order and print the $k$-th one (ranks start at $1$).

For example, with $n = 3$ the permutations are

$$123,\ 132,\ 213,\ 231,\ 312,\ 321$$

and the $3$-rd one is $213$.

### Input

A single line with two integers $n$ and $k$, separated by a space.

### Output

Print one line with $n$ integers: the $k$-th permutation, separated by single spaces.

### Constraints

- $1 \le n \le 9$
- $1 \le k \le n!$ (where $9! = 362880$)
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
3 3
```

**Output**

```
2 1 3
```

### Sample explanation

For $n = 3$ the permutations in lexicographic order are $123, 132, 213, 231, 312, 321$; the $3$-rd is $213$, so the output is `2 1 3`.
