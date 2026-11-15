    static int parseCode(String text) {
        return (text.charAt(0) - '0') * 1000 + (text.charAt(1) - '0') * 100
             + (text.charAt(2) - '0') * 10 + (text.charAt(3) - '0');
    }

    static long solve(String start, String target, long n, String[] dead) {
        boolean[] blocked = new boolean[10000];
        for (String code : dead) blocked[parseCode(code)] = true;
        int begin = parseCode(start);
        int goal = parseCode(target);
        if (blocked[begin] || blocked[goal]) return -1;
        if (begin == goal) return 0;
        int[] dist = new int[10000];
        Arrays.fill(dist, -1);
        int[] queue = new int[10000];
        int head = 0, tail = 0;
        dist[begin] = 0;
        queue[tail++] = begin;
        int[] power = {1, 10, 100, 1000};
        while (head < tail) {
            int cur = queue[head++];
            int step = dist[cur] + 1;
            for (int p : power) {
                int digit = (cur / p) % 10;
                int[] nexts = {(digit + 1) % 10, (digit + 9) % 10};
                for (int nd : nexts) {
                    int nxt = cur + (nd - digit) * p;
                    if (dist[nxt] == -1 && !blocked[nxt]) {
                        dist[nxt] = step;
                        if (nxt == goal) return step;
                        queue[tail++] = nxt;
                    }
                }
            }
        }
        return -1;
    }
