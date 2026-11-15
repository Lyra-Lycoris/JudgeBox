# Twice the Polygon Area

Given the $n$ vertices of a simple polygon (no two edges cross), listed in clockwise or counter-clockwise order, compute **twice** the area of the polygon and output it.

Let $S$ be the area. Output the integer $2S$. Since all vertices have integer coordinates, the shoelace formula guarantees that $2S$ is an integer (a triangle of area $2.5$ has $2S = 5$), so the answer is never fractional.

### Input

- The first line contains one integer $n$, the number of vertices.
- The second line contains $n$ integers $x_1, x_2, \dots, x_n$: the $x$-coordinates of the vertices, in order.
- The third line contains $n$ integers $y_1, y_2, \dots, y_n$: the $y$-coordinates of the vertices, in order.

The $i$-th vertex is $(x_i, y_i)$. That is, the $x$-coordinates and the $y$-coordinates are given **separately**, separated by single spaces.

### Output

One integer: twice the area, that is $2S$, with $2S \ge 0$. A negative number is not acceptable (the area itself is non-negative), so output the absolute value.

### Constraints

$3 \le n \le 200000$ and $-10^6 \le x_i, y_i \le 10^6$.

Each cross term $x_i y_{i+1} - x_{i+1} y_i$ has absolute value at most $2 \times 10^{12}$, and the total sum is at most $4 \times 10^{17}$, which fits in a signed 64-bit integer.

### Sample explanation

The sample is the triangle with vertices $(0,0)$, $(4,0)$ and $(0,3)$ in this order. It is a right triangle with legs $4$ and $3$, so its area is
$$S = \frac{1}{2}\cdot 4 \cdot 3 = 6,$$
hence the output is $2S = 12$.

Checking with the shoelace formula:
$$\sum_{i=1}^{n}\left(x_i y_{i+1} - x_{i+1} y_i\right) = (0\cdot 0 - 4\cdot 0) + (4 \cdot 3 - 0\cdot 0) + (0\cdot 0 - 0\cdot 3) = 12.$$

### Hint

The shoelace formula:
$$2S = \left| \sum_{i=1}^{n} \left( x_i y_{i+1} - x_{i+1} y_i \right) \right|, \quad (x_{n+1}, y_{n+1}) = (x_1, y_1).$$

The vertices may be given clockwise or counter-clockwise, so take the absolute value. The polygon may be concave and may have area $0$ (all vertices equal or all collinear). The time complexity is $O(n)$.
