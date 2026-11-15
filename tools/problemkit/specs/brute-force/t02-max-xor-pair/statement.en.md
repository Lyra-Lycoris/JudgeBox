# Maximum XOR Pair

Given a sequence of non-negative integers $a_1, a_2, \dots, a_n$ of length $n$, find the maximum bitwise XOR over all pairs:

$$\max_{1 \le i < j \le n} \left(a_i \oplus a_j\right)$$

where $\oplus$ denotes bitwise XOR.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by spaces.

### Output

Print a single integer: the maximum XOR value. If $n < 2$, print `0`.

### Constraints

- $1 \le n \le 2000$
- $0 \le a_i \le 10^9$
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
3
1 2 3
```

**Output**

```
3
```

### Sample explanation

Here $a = \{1, 2, 3\}$. The three pairwise XOR values are $1 \oplus 2 = 3$, $1 \oplus 3 = 2$ and $2 \oplus 3 = 1$, so the maximum is $3$ and the output is `3`.
