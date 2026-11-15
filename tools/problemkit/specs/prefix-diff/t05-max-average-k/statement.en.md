# Maximum Average of a Segment of Length at Least K

You are given an integer sequence $a_1, a_2, \dots, a_n$ and an integer $k$. Among all contiguous segments of length **at least** $k$, find the maximum average

$$M = \max_{\substack{1 \le l \le r \le n \\ r - l + 1 \ge k}} \frac{a_l + a_{l+1} + \dots + a_r}{r - l + 1}.$$

Since $M$ may not be an integer, output $1000$ times $M$ rounded down:

$$\text{ans} = \left\lfloor 1000 \cdot M \right\rfloor,$$

that is, output the largest integer $t$ with $M \ge \dfrac{t}{1000}$ (this also holds for negative values).

### Input

The first line contains two integers $n, k$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

### Output

One integer: $\lfloor 1000 \cdot M \rfloor$.

### Constraints

- $1 \le k \le n \le 10^5$
- $-10^9 \le a_i \le 10^9$
- The answer satisfies $|\text{ans}| \le 10^{12}$

### Sample explanation

The sequence is $1, 12, -5, -6, 50$ and $k = 2$. Among segments of length at least $2$ the largest average is attained by $[-6, 50]$, whose average is $22$, so the output is $\lfloor 1000 \cdot 22 \rfloor = 22000$.

### Hint

To test whether some segment of length at least $k$ has average at least $t/1000$, subtract $t/1000$ from every element and check whether some segment of length at least $k$ has a non-negative sum. To avoid floating point errors, multiply everything by $1000$ and work with integers only; prefix sums plus the minimum prefix with index distance at least $k$ give an $O(n)$ test.
