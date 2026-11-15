# Subset Sum Reachability

Given $n$ integers $a_1, a_2, \dots, a_n$ and one integer $target$, decide whether some subset of them (possibly the empty subset) has sum exactly $target$.

The empty subset sums to $0$, so the answer is always `YES` when $target = 0$.

### Input

The first line contains two integers $target$ and $n$, separated by a space.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by spaces.

### Output

Print a single line: `YES` if such a subset exists, otherwise `NO`.

### Constraints

- $1 \le n \le 20$
- $-10^9 \le a_i \le 10^9$
- $-10^{10} \le target \le 10^{10}$
- The sum of any subset fits in a signed 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
6 4
1 2 3 4
```

**Output**

```
YES
```

### Sample explanation

Here $target = 6$, $n = 4$ and $a = \{1, 2, 3, 4\}$.

The subset $\{1, 2, 3\}$ sums to $1 + 2 + 3 = 6$, and $\{2, 4\}$ also sums to $6$, so the answer is `YES`.
