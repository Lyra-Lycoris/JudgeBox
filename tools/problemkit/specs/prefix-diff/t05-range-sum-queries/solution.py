def solve(n: int, a: list[int], l: int, r: int) -> int:
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]
    return pre[r] - pre[l - 1]
