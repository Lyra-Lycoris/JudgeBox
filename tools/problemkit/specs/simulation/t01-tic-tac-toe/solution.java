    static final int[][] LINES = {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6},
                                  {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}};

    static long solve(long[] moves) {
        long[] board = new long[9];
        for (int step = 0; step < 9; ++step) {
            board[(int) moves[step] - 1] = 1 + step % 2;
            for (int[] line : LINES) {
                long a = board[line[0]];
                long b = board[line[1]];
                long c = board[line[2]];
                if (a != 0 && a == b && b == c) return step + 1;
            }
        }
        return 0;
    }
