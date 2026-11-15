# Minimum Jump Cost with a Monotone Queue

There are $n$ stones in a row, numbered $1, 2, \dots, n$; stone $i$ has weight $a_i$. Weights may be negative, meaning that standing on such a stone gives you a profit of $-a_i$ instead of a cost.

You start on stone $1$ and must finish on stone $n$. Standing on stone $i$ costs $a_i$ (the start and the finish each cost once). From stone $i$ you may jump to any stone among $i+1, i+2, \dots, i+k$, but you may not jump past stone $n$.

Find the minimum total cost of a route from stone $1$ to stone $n$.

### Input

The first line contains two integers $n$ and $k$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

### Output

A single line with one integer: the minimum total cost.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le k \le n$
- $-10^9 \le a_i \le 10^9$
- The absolute value of the answer is at most $2 \times 10^{14}$, which fits in a 64-bit integer
- Time limit 2000 ms, memory limit 256 MB

### Sample explanation

Sample 1: $n=6,\ k=2$ and the weights are $1, 3, 2, 5, 4, 1$.

The optimal route is $1 \to 3 \to 5 \to 6$ with total cost $a_1 + a_3 + a_5 + a_6 = 1 + 2 + 4 + 1 = 8$.

Evaluating the transition $\mathrm{dp}[i] = a_i + \min\limits_{i-k \le j < i} \mathrm{dp}[j]$ directly costs $O(nk)$. The left end of the window $[i-k, i-1]$ moves monotonically, so a monotone queue that keeps the $\mathrm{dp}$ values increasing gives the window minimum in $O(1)$ amortized time and the whole DP runs in $O(n)$.
