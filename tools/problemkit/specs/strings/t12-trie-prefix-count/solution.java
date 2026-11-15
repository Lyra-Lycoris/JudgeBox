    static long[] solve(long n, String[] words, long q, String[] queries) {
        int total = 0;
        for (String w : words) total += w.length();
        int capacity = total + 2;
        int[] child = new int[capacity * 26];
        int[] passing = new int[capacity];
        int used = 0;
        for (String w : words) {
            int current = 0;
            for (int i = 0; i < w.length(); ++i) {
                int key = current * 26 + (w.charAt(i) - 'a');
                if (child[key] == 0) child[key] = ++used;
                current = child[key];
                ++passing[current];
            }
        }
        long[] answer = new long[(int) q];
        for (int j = 0; j < q; ++j) {
            String query = queries[j];
            int current = 0;
            boolean found = true;
            for (int i = 0; i < query.length(); ++i) {
                int nxt = child[current * 26 + (query.charAt(i) - 'a')];
                if (nxt == 0) {
                    found = false;
                    break;
                }
                current = nxt;
            }
            answer[j] = found ? passing[current] : 0;
        }
        return answer;
    }
