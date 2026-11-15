# Prime Counting with a Sieve

You are given $n$ positive integers $x_1, x_2, \dots, x_n$. For every $x_i$, count how many primes are less than or equal to $x_i$.

For example, the primes $\le 10$ are $2, 3, 5, 7$, so there are $4$ of them, and there are $25$ primes $\le 100$.

There are many queries and the values are large, so testing each query separately by trial division is too slow. The intended solution precomputes all primes up to $\max x_i$ with a sieve of Eratosthenes (or a linear sieve), then answers each query by binary search (or by prefix counting).

### Input

The first line contains one integer $n$, the number of queries.

The second line contains $n$ integers $x_1, x_2, \dots, x_n$ separated by single spaces. The data may be split over several lines; any whitespace works as a separator.

### Output

Print one line with $n$ integers separated by single spaces, where the $i$-th integer is the number of primes not exceeding $x_i$.

### Constraints

$1 \le n \le 200000$, $1 \le x_i \le 10^7$.

The intended complexity is $O(\max x_i \log\log \max x_i + n \log \max x_i)$.

### Sample explanation

The three queries are $10, 1, 100$:

- the primes $\le 10$ are $2, 3, 5, 7$, so there are $4$;
- no prime is $\le 1$, so there are $0$;
- there are $25$ primes $\le 100$.

Therefore the output is `4 0 25`.
