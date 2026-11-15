# Date After K Days

You are given a valid date: year $y$, month $m$, day $d$, and a non-negative integer $k$. Find the date that is exactly $k$ days after this date.

### Input

A single line with four integers $y, m, d, k$, separated by single spaces.

### Output

One line with the resulting date formatted as `YYYY-MM-DD`: the year is written with at least four digits (padded with leading zeros on the left), the month and the day with exactly two digits each. If the resulting year is greater than $9999$, print all of its digits, e.g. `10000-01-01`.

### Constraints

$1 \le y \le 9999$, $1 \le m \le 12$, $1 \le d \le$ number of days in that month, $0 \le k \le 10^6$. The given date is always valid.

A leap year is a year divisible by $4$ but not by $100$, or divisible by $400$.

### Sample explanation

Sample 1: 2024 is a leap year, so one day after 2024-02-28 is the leap day 2024-02-29.

Sample 2: 1900 is divisible by $100$ but not by $400$, so it is not a leap year; one day after 1900-02-28 is 1900-03-01.
