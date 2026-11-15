# Josephus Problem Survivor

$n$ people stand in a circle, numbered $1$ to $n$ clockwise. Starting from person $1$ and moving clockwise, people count $1, 2, 3, \dots$; whoever says $k$ leaves the circle immediately, and the next person starts counting from $1$ again. This repeats until only one person remains. Find the number of the survivor.

**Naive approach**: let $f(i)$ be the zero-based index of the survivor when $i$ people remain. Then

$$f(1) = 0, \qquad f(i) = (f(i-1) + k) \bmod i ,$$

and the answer is $f(n) + 1$ (converting back to 1-based numbering). This recurrence is $O(n)$ and cannot handle $n = 10^{18}$.

**Optimization**: most steps of the recurrence do not wrap around. Suppose the current size is $m$ and the current value is $f$. As long as $f + j k < m + j$ (equivalently $j(k-1) < m - f$), the next $j$ steps only add $k$, so we can skip them all at once:

$$t = \left\lfloor \frac{m - f - 1}{k - 1} \right\rfloor .$$

Advance the size by $t$ steps (and $f$ by $t k$), and only take a single wrapping step when $t = 0$. The total complexity is $O(k \log n)$. Note that for $k = 1$ the denominator is zero and the answer is simply $n$.

### Input

A single line with two integers $n, k$ separated by a single space.

### Output

One line with a single integer: the number of the survivor (1-based).

### Constraints

$1 \le n \le 10^{18}$, $1 \le k \le 10000$.

### Sample explanation

For $n = 5$ and $k = 2$ the people leave in the order $2, 4, 1, 5$ (each round counts $1, 2$ and whoever says $2$ leaves), so person $3$ is the survivor and the output is `3`.
