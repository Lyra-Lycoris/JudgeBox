# Sliding Window Maximum

You are given an integer array $a_0, a_1, \dots, a_{n-1}$ of length $n$ and an integer $k$.

A window of size $k$ starts at the left end of the array and slides one position to the right at a time. The windows cover the index ranges $[0, k-1]$, $[1, k]$, …, $[n-k, n-1]$, so there are $n-k+1$ windows in total. Print the maximum value inside every window.

### Input

- The first line contains two integers $n$ and $k$, separated by a single space.
- The second line contains $n$ integers $a_0, a_1, \dots, a_{n-1}$, separated by single spaces.

### Output

One line with $n-k+1$ integers: the maximum of each window in order, separated by single spaces.

### Constraints

- $1 \le k \le n \le 200000$;
- $|a_i| \le 10^9$.

### Sample explanation

Sample 1: $n = 8$, $k = 3$.

- Window $[0,2]$: $1, 3, -1$, maximum $3$;
- Window $[1,3]$: $3, -1, -3$, maximum $3$;
- Window $[2,4]$: $-1, -3, 5$, maximum $5$;
- Window $[3,5]$: $-3, 5, 3$, maximum $5$;
- Window $[4,6]$: $5, 3, 6$, maximum $6$;
- Window $[5,7]$: $3, 6, 7$, maximum $7$.

The output is `3 3 5 5 6 7`.

Sample 2: $k = 1$, so every window contains a single element and the answer is the array itself.
