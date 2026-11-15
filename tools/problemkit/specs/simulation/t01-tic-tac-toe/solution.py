LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def solve(moves: list[int]) -> int:
    board = [0] * 9
    for step in range(9):
        board[moves[step] - 1] = 1 + step % 2
        for a, b, c in LINES:
            if board[a] != 0 and board[a] == board[b] == board[c]:
                return step + 1
    return 0
