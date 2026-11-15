package t01_tic_tac_toe

func hasLine(board: Array<Int64>): Bool {
    let lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                 [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for (line in lines) {
        let value = board[line[0]]
        if (value != 0 && value == board[line[1]] && value == board[line[2]]) {
            return true
        }
    }
    return false
}

func solve(moves: Array<Int64>): Int64 {
    let board = Array<Int64>(9, repeat: 0)
    for (step in 0..9) {
        board[moves[step] - 1] = 1 + step % 2
        if (hasLine(board)) {
            return step + 1
        }
    }
    return 0
}
