# Largest Rectangle in Histogram

$n$ bars of width $1$ stand side by side on a horizontal line. Bar $i$ has height $h_i$, every bar rests on the ground at height $0$, and there are no gaps between neighbouring bars.

Find the largest rectangle that fits inside this histogram. The rectangle must have sides parallel to the axes and must be fully covered by the bars (it may touch the ground, and its top may stay below the bar tops).

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $h_0, h_1, \dots, h_{n-1}$, separated by single spaces.

### Output

One integer: the area of the largest rectangle.

### Constraints

- $1 \le n \le 200000$;
- $0 \le h_i \le 10^9$.

The answer can be as large as $2 \times 10^{14}$, so a 64-bit integer is required.

### Sample explanation

Sample 1: the heights are $2, 1, 5, 6, 2, 3$. Taking the third and fourth bar ($h_2 = 5$ and $h_3 = 6$), the rectangle can be $5$ high and $2$ wide, giving $5 \times 2 = 10$. Taking all $6$ bars limits the height to $1$ and gives only $6$. The maximum area is $10$.

Sample 2: every bar has height $7$, so taking all $5$ bars gives $7 \times 5 = 35$.
