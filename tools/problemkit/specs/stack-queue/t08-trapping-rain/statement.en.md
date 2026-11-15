# Trapping Rain Water

$n$ bars of width $1$ stand in a row. Bar $i$ has height $h_i$, there are no gaps between neighbouring bars, and every bar rests on the ground at height $0$. After heavy rain, water is trapped in the valleys between the bars.

Compute how many units of rain water the bars can trap in total. The water surface never rises above the shorter of the two surrounding bars, and the bars themselves do not absorb water.

Formally, the water depth above position $i$ is

$$\min\left(\max_{0 \le j \le i} h_j,\ \max_{i \le j < n} h_j\right) - h_i$$

clamped at $0$ from below. The answer is the sum of the water depths over all positions.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $h_0, h_1, \dots, h_{n-1}$, separated by single spaces.

### Output

One integer: the total amount of trapped rain water.

### Constraints

- $1 \le n \le 200000$;
- $0 \le h_i \le 10^9$.

The answer can be as large as $2 \times 10^{14}$, so a 64-bit integer is required.

### Sample explanation

Sample 1: the heights are $0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1$. The water depths are $0, 0, 1, 0, 1, 2, 1, 0, 0, 1, 0, 0$, which sum to $6$.

Sample 2: the heights are $4, 2, 0, 3, 2, 5$. The water depths are $0, 2, 4, 1, 2, 0$, which sum to $9$.
