# Strictly Second Shortest Route

You are given an **undirected** graph with $n$ vertices and $m$ edges; every edge has a positive integer weight. Vertices are numbered $1$ to $n$.

A **route** from $1$ to $n$ may visit the same vertex or the same edge more than once, and its length is the sum of the weights of all edges on it.

Let $d_1$ be the minimum length over all routes from $1$ to $n$. Find the smallest length $d_2$ that is **strictly greater** than $d_1$, i.e. the length of the strictly second shortest route.

### Input

The first line contains two integers $n$ and $m$, separated by a space.

Each of the next $m$ lines contains three integers $u$, $v$ and $w$: an undirected edge between $u$ and $v$ with weight $w$.

### Output

Print one integer: the length of the strictly second shortest route. Print $-1$ if $n$ is unreachable from $1$, or if no route longer than $d_1$ exists.

### Constraints

- $2 \le n \le 20000$, $1 \le m \le 100000$
- $1 \le u, v \le n$, $1 \le w \le 10^9$
- Multiple edges and self-loops are allowed
- The answer is at most $2.1 \times 10^{13}$, which fits in a signed 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample

**Input**

```
4 4
1 2 1
2 4 3
1 3 2
3 4 4
```

**Output**

```
6
```

### Sample explanation

Routes from $1$ to $4$ include:

- $1 \to 2 \to 4$ with length $1 + 3 = 4$, the shortest length $d_1 = 4$;
- $1 \to 3 \to 4$ with length $2 + 4 = 6$;
- $1 \to 2 \to 1 \to 2 \to 4$ with length $1 + 1 + 1 + 3 = 6$;
- every other route is longer than $6$.

The smallest length strictly greater than $4$ is $6$, so the answer is `6`.
