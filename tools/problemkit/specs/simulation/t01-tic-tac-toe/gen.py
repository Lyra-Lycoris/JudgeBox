import random

LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def _first_win(moves):
    board = [0] * 9
    for step in range(9):
        board[moves[step] - 1] = 1 + step % 2
        for a, b, c in LINES:
            if board[a] != 0 and board[a] == board[b] == board[c]:
                return step + 1
    return 0


def cases():
    fixed = [
        "1 4 2 5 3 6 7 8 9",   # X 第五步一行
        "1 2 3 5 4 6 8 7 9",   # 平局
        "1 4 2 5 9 6 3 7 8",   # O 第六步一行
        "5 1 9 2 3 6 4 7 8",   # 斜线
        "1 2 4 5 9 3 6 7 8",   # 列
        "2 5 3 6 4 7 1 8 9",   # 列
    ]
    rng = random.Random(20261114)
    seen = set()
    extra = []
    while len(extra) < 6:
        perm = list(range(1, 10))
        rng.shuffle(perm)
        key = tuple(perm)
        if key in seen:
            continue
        seen.add(key)
        extra.append(" ".join(str(x) for x in perm))
    out = []
    for index, text in enumerate(fixed + extra):
        out.append({"id": "%02d" % (index + 1), "input": text + "\n"})
    return out
