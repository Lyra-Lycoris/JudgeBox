# Longest Common Prefix

You are given $k$ non-empty lowercase strings $w_1, w_2, \ldots, w_k$.

Compute the length of their longest common prefix, that is, the largest integer $L$ such that the first $L$ characters of every string are identical:

$$w_1[1..L] = w_2[1..L] = \cdots = w_k[1..L].$$

For example, the longest common prefix of `flower`, `flow` and `flight` is `fl`, of length $2$.

### Input

- The first line contains one integer $k$, the number of strings.
- The second line contains $k$ space-separated lowercase strings $w_1, w_2, \ldots, w_k$.

### Output

Print one integer: the length of the longest common prefix. If the strings do not even share their first character, print `0`.

### Constraints

- $1 \le k \le 2 \times 10^5$.
- Every string is non-empty and consists of lowercase English letters `a` to `z` only.
- The sum of the lengths of all strings is at most $2 \times 10^5$.

### Sample explanation

Sample 1: $k = 3$ with strings `flower`, `flow`, `flight`.

- All three start with `f`, so we can continue;
- all three have `l` second, so we can continue;
- the third characters are `o`, `o`, `i`, which are not all equal, so we must stop.

The longest common prefix is `fl` with length $2$, so the answer is `2`.
