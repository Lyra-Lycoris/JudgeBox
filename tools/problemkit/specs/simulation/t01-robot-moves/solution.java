    static long[] solve(String s) {
        long[] dx = {0, 1, 0, -1};
        long[] dy = {1, 0, -1, 0};
        int facing = 0;
        long x = 0, y = 0;
        for (int i = 0; i < s.length(); ++i) {
            char ch = s.charAt(i);
            if (ch == 'L') {
                facing = (facing + 3) % 4;
            } else if (ch == 'R') {
                facing = (facing + 1) % 4;
            } else if (ch == 'F') {
                x += dx[facing];
                y += dy[facing];
            } else if (ch == 'B') {
                x -= dx[facing];
                y -= dy[facing];
            }
        }
        return new long[] {x, y};
    }
