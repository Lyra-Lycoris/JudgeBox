# Square Root Rounded to Three Decimals

Given a non-negative integer $x$, compute $\sqrt{x}$ and **round** it to $3$ decimal places.

To avoid any floating-point output issues, print the rounded value multiplied by $1000$, that is:

$$\left\lfloor 1000\sqrt{x} + 0.5 \right\rfloor$$

### Input

One line with a single integer $x$.

### Output

One integer: $\lfloor 1000\sqrt{x} + 0.5 \rfloor$.

### Constraints

- $0 \le x \le 10^{12}$

### Sample explanation

For $x = 7$, $\sqrt{7} \approx 2.6457513$.

Rounded to three decimals this is $2.646$ (the fourth decimal digit is $7$, so it rounds up). Multiplying by $1000$ gives $2646$, so the answer is $2646$.

The value can be found by binary searching on the real line: the answer $m$ satisfies $1000\sqrt{x} \ge m - 0.5$, and after squaring both sides this becomes the integer inequality $(2m-1)^2 \le 4x \cdot 10^6$, which can be compared exactly without floating-point error. Note that the answer for $x = 0$ is $0$.

Also, since $x$ is an integer, $1000\sqrt{x}$ can never equal $k + 0.5$: otherwise $\sqrt{x}$ would be rational, $x$ would be a perfect square, and $1000\sqrt{x}$ would be an integer. So there is no exact half-way tie.
