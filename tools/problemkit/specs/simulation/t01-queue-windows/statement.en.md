# Queue Simulation with Windows

A bank has $k$ service windows. Customer $i$ arrives at time $a_i$ and needs $s_i$ time units of service.

Customers are served in arrival order (the sequence $a_i$ is non-decreasing). Each customer goes to the window that becomes free first; if several windows are free at the same moment, the one with the smallest index is chosen (this never changes the answer). A customer who arrives while every window is busy waits until a window becomes free.

The waiting time of a customer is (the moment service starts) − (the moment they arrive). Compute the total waiting time over all customers.

### Input

- The first line contains two integers $n$ and $k$, separated by a single space.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.
- The third line contains $n$ integers $s_1, s_2, \dots, s_n$, separated by single spaces.

### Output

One integer: the total waiting time.

### Constraints

$1 \le n \le 200000$, $1 \le k \le 200000$, $0 \le a_i \le 10^9$ with $a_1 \le a_2 \le \dots \le a_n$, and $0 \le s_i \le 10^9$.

It is guaranteed that the total waiting time is at most $10^{18}$, so a 64-bit integer is enough.

### Sample explanation

Sample 1: $n = 3$, $k = 1$, arrival times $0, 2, 5$ and service times $4, 4, 4$.

- Customer $1$ starts at $0$ and waits $0$.
- Customer $2$ arrives at $2$, but the only window is busy until $4$, so they wait $2$ and leave at $8$.
- Customer $3$ arrives at $5$ and starts at $8$, so they wait $3$.

The answer is $0 + 2 + 3 = 5$.

Sample 2: there are $5$ windows but only $3$ customers, so everybody starts immediately and the answer is $0$.
