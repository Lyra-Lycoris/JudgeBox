# Run-Length Encoded Length Queries

Run-length encoding (RLE) is the simplest compression: maximal blocks of equal characters are written as "the character followed by the length of the block".

This problem uses the following exact rule. For every maximal block of equal characters in a string, let its length be $c$:

- if $c = 1$, the encoding contains just that character, taking $1$ character position;
- if $c \ge 2$, the encoding contains the character followed by the decimal representation of $c$, taking $1 + \operatorname{digits}(c)$ character positions, where $\operatorname{digits}(c)$ is the number of decimal digits of $c$ (for example $\operatorname{digits}(9)=1$, $\operatorname{digits}(10)=2$, $\operatorname{digits}(200000)=6$).

For instance, `aaabbc` splits into `aaa`, `bb`, `c` with lengths $3, 2, 1$, so its encoding is `a3b2c` and the encoded length is $2 + 2 + 1 = 5$.

You are given a string $s$ of length $n$ and $q$ queries. Each query gives $l, r$ ($1 \le l \le r \le n$); compute the **RLE length of the substring $s[l..r]$**. Only the substring itself matters: the blocks at its two ends may be truncated, and must be re-measured with their truncated lengths.

### Input

- The first line contains one integer $n$.
- The second line contains a lowercase string $s$ of length $n$.
- The third line contains one integer $q$.
- The next $q$ lines each contain two integers $l, r$, describing one query.

### Output

Print one line with $q$ space-separated integers, the answers of the queries in order.

### Constraints

- $1 \le n \le 2 \times 10^5$ and $1 \le q \le 2 \times 10^5$.
- $1 \le l \le r \le n$.
- $s$ consists of lowercase English letters `a` to `z` only.

### Sample explanation

Sample 1: $n = 6$, $s = \text{aaabbc}$, $q = 4$.

- Query $[1,6]$: substring `aaabbc`, encoding `a3b2c`, length $2+2+1 = 5$;
- query $[1,3]$: substring `aaa`, encoding `a3`, length $2$;
- query $[4,6]$: substring `bbc`, encoding `b2c`, length $2+1 = 3$;
- query $[1,1]$: substring `a`, encoding `a`, length $1$.

Hence the output is `5 2 3 1`.
