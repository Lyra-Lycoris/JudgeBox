# Maximise the Minimum Segment Sum

You are given $n$ positive integers $a_1, a_2, \dots, a_n$ and an integer $k$ with $1 \le k \le n$.

Split the whole sequence into **exactly $k$ contiguous non-empty segments**: choose indices

$$0 = p_0 < p_1 < p_2 < \dots < p_k = n,$$

so that segment $i$ is $a_{p_{i-1}+1}, \dots, a_{p_i}$, and let

$$s_i = \sum_{j=p_{i-1}+1}^{p_i} a_j .$$

Let $M = \min(s_1, s_2, \dots, s_k)$. Choose the split that makes $M$ **as large as possible** and output that maximum $M$.

### Input

- The first line contains two integers $n$ and $k$.
- The second line contains $n$ positive integers $a_1, a_2, \dots, a_n$ separated by single spaces.

### Output

One integer: the largest possible value of $M$.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le k \le n$
- $1 \le a_i \le 10^9$, hence $\sum a_i \le 2 \times 10^{14}$ and the answer is at most $2 \times 10^{14}$

### Sample explanation

For $n = 5$, $k = 3$ and $a = (1, 2, 3, 4, 5)$, the split $(1,2,3)\mid(4)\mid(5)$ gives segment sums $6, 4, 5$, whose minimum is $4$.

Making the minimum $5$ is impossible: the element $4$ alone is smaller than $5$, so it must be merged with another element, and then at most two segments can be produced. Hence the answer is `4`.

### Hint

The answer is monotone: if every segment can be made at least $x$, the same holds for any smaller value, so binary search on the answer.

To test a candidate $x$, scan from left to right and cut a segment as soon as the running sum reaches $x$; let $c$ be the number of segments produced this way (a trailing remainder smaller than $x$ is ignored). Then $x$ is feasible **if and only if** $c \ge k$: when $c \ge k$, merge segment $k$ with everything after it, which only increases its sum; and conversely, any valid split into $k$ segments yields at least as many greedy cuts.
