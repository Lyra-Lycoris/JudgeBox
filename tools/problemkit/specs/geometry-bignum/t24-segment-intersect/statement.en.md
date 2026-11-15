# Do Two Segments Intersect?

Two segments $AB$ and $CD$ in the plane are given, where $A(x_A,y_A)$, $B(x_B,y_B)$, $C(x_C,y_C)$ and $D(x_D,y_D)$ are integer points. Decide whether the two segments **share at least one point**.

The segments are closed: both endpoints belong to the segment. Therefore all of the following count as intersecting:

- the segments properly cross in their interiors;
- an endpoint of one segment lies on the other segment (including lying on its endpoint);
- the segments are collinear and overlap (including overlapping in a single endpoint only);
- one segment is degenerate (a single point) and that point lies on the other segment.

### Input

- The first line contains one integer $T$, the number of queries.
- Each of the next $T$ lines contains eight integers $x_A, y_A, x_B, y_B, x_C, y_C, x_D, y_D$ describing one query.

### Output

Print $T$ lines. For each query print `YES` if the two segments share a point, otherwise print `NO`.

### Constraints

$1 \le T \le 100000$ and $-10^9 \le x_A, y_A, x_B, y_B, x_C, y_C, x_D, y_D \le 10^9$.

Every coordinate difference has absolute value at most $2 \times 10^9$ and every cross product has absolute value at most $8 \times 10^{18}$, which fits in a signed 64-bit integer.

### Sample explanation

The sample contains six queries:

1. $(0,0)-(4,4)$ and $(0,4)-(4,0)$ properly cross at $(2,2)$, so `YES`;
2. $(0,0)-(4,0)$ and $(4,0)-(4,4)$ share the endpoint $(4,0)$, so `YES`;
3. $(0,0)-(4,0)$ and $(0,1)-(4,1)$ are parallel and disjoint, so `NO`;
4. $(0,0)-(4,0)$ and $(1,0)-(3,0)$ are collinear with an overlap, so `YES`;
5. $(0,0)-(1,0)$ and $(2,0)-(3,0)$ are collinear but disjoint, so `NO`;
6. the degenerate segment at $(2,2)$ and $(0,0)-(4,4)$: the point lies on the segment, so `YES`.

### Hint

Let
$$\text{cross}(P,Q,R) = (x_Q-x_P)(y_R-y_P) - (y_Q-y_P)(x_R-x_P),$$
the cross product of $\overrightarrow{PQ}$ and $\overrightarrow{PR}$, and put
$$d_1=\text{cross}(A,B,C),\quad d_2=\text{cross}(A,B,D),\quad d_3=\text{cross}(C,D,A),\quad d_4=\text{cross}(C,D,B).$$

- If $d_1$ and $d_2$ have opposite signs and $d_3$ and $d_4$ also have opposite signs, the segments properly cross, so the answer is `YES`;
- otherwise, if some $d_i = 0$ (the corresponding point is collinear with the corresponding segment) and that point lies inside the bounding box of the segment (both coordinates between the endpoint coordinates), the answer is `YES`;
- otherwise the answer is `NO`.

Each query is $O(1)$, hence $O(T)$ in total.
