# Minimum Ship Capacity

A ship must transport $n$ packages, where the $i$-th package weighs $w_i$. The packages must be shipped **in the given order**.

The ship sails once per day and can load a contiguous block of the remaining packages, because the packages are stacked in order. The ship has a fixed daily capacity $C$: the total weight loaded on one day must not exceed $C$.

Find the minimum capacity $C$ that allows all packages to be transported within $d$ days (inclusive).

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $w_1, w_2, \dots, w_n$.

The third line contains one integer $d$.

### Output

One integer: the minimum feasible capacity $C$.

### Constraints

- $1 \le d \le n \le 2 \times 10^5$
- $1 \le w_i \le 10^9$
- $\sum w_i \le 2 \times 10^{14}$ is guaranteed, so the answer fits in a 64-bit integer

### Sample explanation

With $n = 10$, weights $1, 2, \dots, 10$, and $d = 5$ days:

- For $C = 14$, greedy loading in order gives day 1: $1+2+3+4 = 10$, day 2: $5+6 = 11$, day 3: $7$, day 4: $8$, day 5: $9$, and the last package $10$ needs a sixth day, which exceeds $5$ days.
- For $C = 15$: day 1: $1+2+3+4+5 = 15$, day 2: $6+7 = 13$, day 3: $8$, day 4: $9$, day 5: $10$, exactly $5$ days.

Hence the minimum capacity is $15$.

To test a capacity $C$, greedy loading in order is optimal: load as much as possible each day. The number of days needed never increases as $C$ grows, so the answer can be found by binary search.
