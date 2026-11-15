# Multi-key Score Ranking

There are $n$ students. Each student has a student ID and scores in three subjects: Chinese, mathematics and English. Rank the students from best to worst using the following priority rules, then output their IDs in ranked order:

1. a higher total score (Chinese + mathematics + English) comes first;
2. if the totals are equal, a higher Chinese score comes first;
3. if the Chinese scores are also equal, a smaller student ID comes first.

All student IDs are distinct, so the ranking is unique.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers: the student IDs of students $1$ to $n$.
- The third line contains $n$ integers: their Chinese scores.
- The fourth line contains $n$ integers: their mathematics scores.
- The fifth line contains $n$ integers: their English scores.

Numbers on the same line are separated by single spaces.

### Output

One line with $n$ integers: the student IDs in ranked order, separated by single spaces.

### Constraints

$1 \le n \le 200000$, $1 \le$ ID $\le 10^9$ with all IDs distinct, and $0 \le$ each score $\le 100$.

### Sample explanation

Sample 1: the four students are

| ID | Chinese | Mathematics | English | Total |
| --- | --- | --- | --- | --- |
| 3 | 90 | 80 | 70 | 240 |
| 1 | 90 | 70 | 80 | 240 |
| 4 | 80 | 100 | 60 | 240 |
| 2 | 70 | 60 | 60 | 190 |

The first three students all have a total of $240$. Students 1 and 3 also tie on Chinese ($90$ each), so the smaller ID comes first. The ordering is 1, 3 (then 4 with Chinese $80$) and finally 2, so the answer is `1 3 4 2`.
