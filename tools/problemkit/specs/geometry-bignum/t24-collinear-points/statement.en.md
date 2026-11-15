# Are the Three Points Collinear?

Three integer points $A(x_1,y_1)$, $B(x_2,y_2)$ and $C(x_3,y_3)$ are given. Decide whether all three of them lie on one and the same straight line.

Convention: if two of the points coincide (or even if all three coincide), the answer is still **collinear** — take the line through the location of the coincident pair and the third point; it contains all three points. Equivalently, the three points are collinear if and only if some straight line passes through all of them.

### Input

- The first line contains one integer $T$, the number of queries.
- Each of the next $T$ lines contains six integers $x_1, y_1, x_2, y_2, x_3, y_3$ describing one query.

### Output

Print $T$ lines. For each query print `YES` if the three points are collinear, otherwise print `NO`.

### Constraints

$1 \le T \le 100000$ and $-10^9 \le x_i, y_i \le 10^9$.

Every coordinate difference has absolute value at most $2 \times 10^9$, and the absolute value of the cross product of a query is at most $8 \times 10^{18}$, so a signed 64-bit integer is enough.

### Sample explanation

The sample contains four queries and prints `YES`, `NO`, `YES`, `YES`:

1. $(0,0),(1,1),(2,2)$: all three points lie on $y=x$, so they are collinear;
2. $(0,0),(1,1),(2,3)$: the third point is not on the line through the first two points;
3. $(0,0),(0,5),(0,-7)$: all three points lie on the vertical line $x=0$;
4. $(-3,4),(0,0),(3,-4)$: all three points lie on $y=-\frac{4}{3}x$.

### Hint

Let
$$\text{cross} = (x_2-x_1)(y_3-y_1) - (y_2-y_1)(x_3-x_1),$$
the cross product of $\overrightarrow{AB}$ and $\overrightarrow{AC}$. The three points are collinear if and only if $\text{cross} = 0$. Each query is $O(1)$, so the total time is $O(T)$.

Do not compare slopes: computing a slope needs division, which has a division-by-zero case and loses exactness.
