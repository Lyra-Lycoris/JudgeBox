# Path Node-Weight Sum

You are given an undirected tree with $n$ nodes numbered $1 \sim n$. Each node $i$ has a weight $w_i$, which may be negative.

The path between nodes $u$ and $v$ is the unique simple path connecting them. The **node-weight sum** of a path is the sum of the weights of all nodes on that path, including $u$ and $v$ themselves.

Answer $q$ queries; each gives two nodes $u, v$ and asks for the node-weight sum of the path between them.

### Input

The first line contains an integer $n$.

The second line contains $n$ integers $w_1, w_2, \dots, w_n$.

Each of the following $n-1$ lines contains two integers $u_i, v_i$ describing a tree edge. These lines are absent when $n = 1$.

The next line contains an integer $q$.

Each of the following $q$ lines contains two integers $u, v$ describing one query.

The edges are guaranteed to form a tree.

### Output

One line with $q$ space-separated integers; the $t$-th one is the answer to the $t$-th query.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le q \le 2 \times 10^5$
- $-10^9 \le w_i \le 10^9$
- $1 \le u, v, u_i, v_i \le n$
- The absolute value of any path node-weight sum is at most $2 \times 10^{14}$

### Sample Explanation

$n = 5$ with weights $w = (3, -1, 4, 1, 5)$ and edges $(1,2), (2,3), (2,4), (4,5)$.

- Query $(3, 5)$: the path is $3 \to 2 \to 4 \to 5$ with node-weight sum $4 + (-1) + 1 + 5 = 9$.
- Query $(1, 5)$: the path is $1 \to 2 \to 4 \to 5$ with sum $3 + (-1) + 1 + 5 = 8$.
- Query $(1, 1)$: the path contains only node $1$, so the answer is $3$.

Hence the output is `9 8 3`.
