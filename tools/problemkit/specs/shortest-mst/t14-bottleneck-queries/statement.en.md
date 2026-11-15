# Bottleneck Path Queries

You are given a **connected undirected** graph with $n$ vertices and $m$ edges; every edge has a positive integer weight.

For any two vertices $u, v$, define the **bottleneck value** $\beta(u,v)$ as the smallest possible maximum edge weight along a path from $u$ to $v$:

$$\beta(u,v) = \min_{P: u \to v} \ \max_{e \in P} w(e).$$

If $u = v$, define $\beta(u,u) = 0$.

You are given $q$ queries, each a pair $(u, v)$; answer $\beta(u,v)$ for each of them.

### Input

The first line contains three integers $n$, $m$ and $q$, separated by spaces.

Each of the next $m$ lines contains three integers $u$, $v$ and $w$: an undirected edge between $u$ and $v$ with weight $w$.

Each of the next $q$ lines contains two integers $u$ and $v$: one query.

### Output

Print one line with $q$ integers, separated by spaces: the $i$-th integer is the answer $\beta(u,v)$ for the $i$-th query.

### Constraints

- $2 \le n \le 50000$, $n-1 \le m \le 100000$, $1 \le q \le 50000$
- $1 \le u, v \le n$, $1 \le w \le 10^9$
- The graph is connected; multiple edges and self-loops are allowed
- A query may have $u = v$, in which case the answer is $0$
- Time limit 3000 ms, memory limit 256 MB

### Sample

**Input**

```
4 5 3
1 2 5
2 3 4
3 4 6
1 3 10
2 4 2
1 4
1 3
3 4
```

**Output**

```
5 5 4
```

### Sample explanation

The minimum spanning tree of the graph consists of the edges $2-4$ ($2$), $2-3$ ($4$) and $1-2$ ($5$), with total weight $11$.

- Query $(1,4)$: the tree path is $1 \to 2 \to 4$ with maximum edge weight $\max(5,2) = 5$; the route $1 \to 3 \to 4$ has maximum edge weight $10$, so the answer is $5$.
- Query $(1,3)$: the tree path $1 \to 2 \to 3$ has maximum edge weight $\max(5,4) = 5$, better than the direct edge $1-3$ of weight $10$, so the answer is $5$.
- Query $(3,4)$: the tree path $3 \to 2 \to 4$ has maximum edge weight $\max(4,2) = 4$, so the answer is $4$.

Hence the output is `5 5 4`.
