# Gas Station Circuit Start

There are $n$ gas stations on a circular road. Station $i$ provides $gas_i$ liters of fuel, and driving from station $i$ to station $i+1$ (station $n-1$ leads back to station $0$) consumes $cost_i$ liters.

You drive a car with an empty tank, start at some station (refueling there first) and travel clockwise. The tank has unlimited capacity. Find the index of a station from which you can complete one full lap and return to the start. The index is 0-based. Output $-1$ if no such station exists. When a solution exists, it is guaranteed to be unique.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $gas_0, gas_1, \dots, gas_{n-1}$.

The third line contains $n$ integers $cost_0, cost_1, \dots, cost_{n-1}$.

### Output

One integer: a valid starting index ($0$ to $n-1$), or $-1$ if the lap is impossible.

### Constraints

- $1 \le n \le 10^5$
- $0 \le gas_i, cost_i \le 10^4$

### Sample explanation

With $n=5$, the fuel amounts are $1,2,3,4,5$ and the costs are $3,4,5,1,2$. Total fuel equals total cost, so a solution exists. Starting at $0$, $1$ or $2$ the tank immediately drops below zero ($1-3<0$). Starting at $3$ the running fuel is $3, 4, 1, 2$ after each edge, never negative, so index 3 is the answer.
