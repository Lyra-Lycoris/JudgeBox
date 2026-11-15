    static long[] solve(long n, long[] a) {
        PriorityQueue<Long> low = new PriorityQueue<Long>(Collections.reverseOrder());
        PriorityQueue<Long> high = new PriorityQueue<Long>();
        long[] answer = new long[(int) n];
        for (int i = 0; i < (int) n; ++i) {
            long x = a[i];
            if (low.isEmpty() || x <= low.peek()) low.add(x);
            else high.add(x);
            long target = (i + 2) / 2;
            while (low.size() > target) high.add(low.poll());
            while (low.size() < target) low.add(high.poll());
            answer[i] = low.peek();
        }
        return answer;
    }
