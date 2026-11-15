# Number of Convex Hull Vertices

Given $n$ integer points in the plane, compute the **number of vertices of their convex hull**.

The convex hull is the smallest convex polygon containing all given points. Conventions:

- if all points coincide, the hull degenerates to a point and the answer is $1$;
- if all points lie on one straight line (and are not all equal), the hull degenerates to a segment and the answer is $2$;
- otherwise the hull is a convex polygon, and **points lying strictly inside one of its edges are not vertices** (only the "corners" are counted).

### Input

- The first line contains one integer $n$, the number of points.
- The second line contains $n$ integers $x_1, x_2, \dots, x_n$: the $x$-coordinates of the points, in order.
- The third line contains $n$ integers $y_1, y_2, \dots, y_n$: the $y$-coordinates of the points, in order.

The $i$-th point is $(x_i, y_i)$; the $x$- and $y$-coordinates are given **separately**. Points may repeat.

### Output

One integer: the number of vertices of the convex hull.

### Constraints

$1 \le n \le 200000$ and $-10^9 \le x_i, y_i \le 10^9$.

Every coordinate difference has absolute value at most $2 \times 10^9$, and every cross product (a difference of two products) has absolute value at most $8 \times 10^{18}$, which fits in a signed 64-bit integer.

### Sample explanation

The sample contains $6$ points: $(0,0),(4,0),(4,4),(0,4),(2,2),(1,1)$.

The points $(0,0),(4,0),(4,4),(0,4)$ form the four corners of a square, while $(2,2)$ and $(1,1)$ lie strictly inside that square and cannot be hull vertices. The hull is therefore the square, and it has $4$ vertices.

### Hint

Use Andrew's monotone chain algorithm:

1. sort all points lexicographically by $(x,y)$ and remove duplicates;
2. scan from left to right, maintaining the "lower hull" on a stack: while the last two points of the stack together with the new point do not make a strictly left turn (cross product $\le 0$), pop the stack;
3. scan from right to left to build the "upper hull";
4. the answer is the sum of the two sizes minus $2$, because the first and the last point are counted twice.

Sorting and scanning are both $O(n \log n)$. Note the comparison must be $\le 0$ so that collinear points inside an edge are dropped, as required.
