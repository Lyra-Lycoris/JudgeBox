# Compare a Point-to-Line Distance with an Integer

A line in the plane is given by two distinct integer points $A(x_1,y_1)$ and $B(x_2,y_2)$. Together with an integer point $P(p_x,p_y)$ and an integer $d$, decide whether **the distance from $P$ to the line $AB$ is at most $d$**.

The distance from $P$ to the line $AB$ is the length of the perpendicular segment from $P$ to the line, that is
$$\text{dist}(P, AB) = \frac{\left| (x_2-x_1)(p_y-y_1) - (y_2-y_1)(p_x-x_1) \right|}{\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}}.$$

### Input

- The first line contains one integer $T$, the number of queries.
- Each of the next $T$ lines contains seven integers $x_1, y_1, x_2, y_2, p_x, p_y, d$ describing one query.

It is guaranteed that $(x_1,y_1) \ne (x_2,y_2)$ in every query, so the line is well defined.

### Output

Print $T$ lines. For each query print `YES` if the distance is at most $d$, otherwise print `NO`. When the distance is exactly $d$, print `YES`.

### Constraints

$1 \le T \le 100000$.

$-10^4 \le x_1, y_1, x_2, y_2, p_x, p_y \le 10^4$ and $0 \le d \le 10^4$.

Under these limits the absolute value of the cross product is at most $8 \times 10^8$, its square is at most $6.4 \times 10^{17}$, and $d^2 \cdot |AB|^2 \le 10^8 \times 8 \times 10^8 = 8 \times 10^{16}$. All arithmetic fits in signed 64-bit integers, **no square root is needed**, and nothing overflows.

### Sample explanation

The sample contains four queries:

1. The line $y=0$ (through $(0,0)$ and $(10,0)$); the distance from $(3,4)$ is $4$, and $4 \le 4$, so the answer is `YES`.
2. The same line and point with $d=3$: $4 > 3$, so `NO`.
3. The point $(5,0)$ lies on the line, so the distance is $0 \le 0$ and the answer is `YES`.
4. The line through $(0,0)$ and $(3,4)$; the distance from $(3,0)$ is $\frac{|3\cdot 0 - 4 \cdot 3|}{5} = \frac{12}{5} = 2.4 > 2$, so `NO`.

### Hint

Squaring both sides turns "the distance is at most $d$" into the integer condition
$$\text{cross}^2 \le d^2 \cdot \left((x_2-x_1)^2+(y_2-y_1)^2\right),$$
where $\text{cross} = (x_2-x_1)(p_y-y_1) - (y_2-y_1)(p_x-x_1)$. The comparison then stays entirely in integers, avoiding floating point errors (compare $2.4$ and $2$ in query 4 of the sample).
