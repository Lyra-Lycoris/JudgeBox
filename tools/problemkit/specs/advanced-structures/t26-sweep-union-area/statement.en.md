# Union Area of Rectangles

You are given $n$ axis-parallel rectangles. Each rectangle is described by the coordinates of its bottom-left corner $(x_1, y_1)$ and top-right corner $(x_2, y_2)$, with $x_1 < x_2$ and $y_1 < y_2$.

Compute the total area covered by the union of the rectangles; parts covered by several rectangles are counted only once.

A possible approach is a sweep line: split every rectangle into a left and a right vertical edge event, sort the events by $x$, and sweep from left to right. After compressing the $y$ coordinates, a segment tree maintains the total covered length, and for every pair of consecutive events we add "covered length × horizontal distance" to the area.

### Input

The first line contains one integer $n$.

Each of the next $n$ lines contains four integers $x_1, y_1, x_2, y_2$ describing one rectangle.

### Output

One integer: the total area covered by all rectangles.

### Constraints

- $1 \le n \le 2000$
- $-10^9 \le x_1 < x_2 \le 10^9$, $-10^9 \le y_1 < y_2 \le 10^9$
- The total area is at most $4 \times 10^{18}$, which fits in a signed 64-bit integer

### Sample explanation

The three rectangles are $[0,2] \times [0,2]$, $[1,3] \times [1,3]$ and $[2,4] \times [0,1]$.

The first two have area $4$ each and the third has area $2$. The first two overlap exactly on $[1,2] \times [1,2]$, an area of $1$. The third rectangle only touches the others along its boundary, so there is no area overlap with them.

Hence the total area is $4 + 4 + 2 - 1 = 9$.
