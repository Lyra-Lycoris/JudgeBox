# Eccentricity of Every Node

You are given a tree with $n$ nodes numbered $1 \sim n$, rooted at node $1$. Every edge has length $1$.

For each node $v$ define

$$e(v) = \max_{1 \le u \le n} \operatorname{dist}(v, u),$$

the maximum distance from $v$ to any node (including $v$ itself, at distance $0$). Compute $e(1), e(2), \dots, e(n)$.

### Input

The first line contains one integer $n$.

The second line contains $n-1$ integers $p_2, p_3, \dots, p_n$, where $p_i$ is the parent of node $i$; it is guaranteed that $1 \le p_i < i$. When $n=1$ this line is empty (nothing is read).

### Output

One line with $n$ integers, the $i$-th of them being $e(i)$, separated by single spaces.

### Constraints

- $1 \le n \le 2 \times 10^5$
- For every $2 \le i \le n$, $1 \le p_i < i$ (so the input always describes a tree rooted at $1$)
- Time limit 2000 ms, memory limit 256 MB

### Sample explanation

Sample 1: $n=5$; node $1$ has children $2, 3$, and node $3$ has children $4, 5$.

- $e(1) = 2$ (to $4$ or $5$);
- $e(2) = 3$ (to $4$ or $5$);
- $e(3) = 2$ (to $2$);
- $e(4) = 3$ (to $2$);
- $e(5) = 3$ (to $2$).

Hence the output is `2 3 2 3 3`.

### Hint

One DFS only gives the downward distances $\mathrm{down}(v)$. The "upward" part is obtained by rerooting:

- First compute $\mathrm{down}(v)$ bottom-up, together with the largest and the second largest value of $\mathrm{down}(c)+1$ among the children $c$ of $v$;
- Then walk top-down: for a node $v$ with parent $f$,
  $$\mathrm{up}(v) = 1 + \max\left(\mathrm{up}(f),\ \text{largest } \mathrm{down}(c)+1 \text{ over the siblings } c\right),$$
  where the sibling maximum is read from the parent's largest/second largest pair in $O(1)$.
- Finally $e(v) = \max(\mathrm{down}(v), \mathrm{up}(v))$. The whole algorithm is $O(n)$.
