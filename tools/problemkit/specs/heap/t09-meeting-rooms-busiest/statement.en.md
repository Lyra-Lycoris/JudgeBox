# Meeting Rooms: Busiest Room

There are $n$ meeting rooms numbered $0$ to $n-1$, all free at time $0$. There are $m$ meetings; meeting $i$ has start time $s_i$ and lasts $d_i$ units of time.

All meetings are handled in increasing order of start time; meetings with the same start time are handled in input order. For each meeting:

- if at least one room is free when the meeting starts, it is placed in the free room with the **smallest index** and starts on time;
- otherwise it is placed in the room that becomes free **earliest** (ties broken by the smallest room index), and it starts at the moment that room becomes free.

A meeting occupies its room during $[\text{actual start},\ \text{actual start} + d_i)$.

Return the index of the room that hosted the **largest** number of meetings; if several rooms tie, return the smallest such index.

### Input

The first line contains two integers $n$ and $m$.

The second line contains $m$ integers $s_1, s_2, \dots, s_m$.

The third line contains $m$ integers $d_1, d_2, \dots, d_m$.

### Output

Print one integer: the busiest room index (smallest index on ties).

### Constraints

- $1 \le n \le 100000$
- $1 \le m \le 200000$
- $0 \le s_i \le 10^9$, $1 \le d_i \le 10^9$

### Sample Explanation

With $n=2$, the four meetings are $(0, 10)$, $(1, 4)$, $(2, 5)$, $(3, 1)$ (start, duration).

- Meeting $1$: both rooms free, use room $0$ for $[0, 10)$.
- Meeting $2$: room $1$ is free, use room $1$ for $[1, 5)$.
- Meeting $3$: at time $2$ no room is free; room $1$ frees up first (at time $5$), so it is used for $[5, 10)$.
- Meeting $4$: at time $3$ no room is free; both rooms free at time $10$, so the smaller index $0$ is used for $[10, 11)$.

Rooms $0$ and $1$ host $2$ meetings each, so the answer is the smaller index $0$.
