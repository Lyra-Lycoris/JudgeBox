    static int modeLowerBound(long[] arr, int len, long x) {
        int lo = 0, hi = len;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (arr[mid] < x) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    static int modeCountIn(int[] p, int l, int r) {
        int lo = 0, hi = p.length;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (p[mid] < l) lo = mid + 1;
            else hi = mid;
        }
        int left = lo;
        lo = 0;
        hi = p.length;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (p[mid] <= r) lo = mid + 1;
            else hi = mid;
        }
        return lo - left;
    }

    static long[] solve(long n, long[] a, long q, long[][] ops) {
        int sz = (int) n;
        long[] values = Arrays.copyOf(a, sz);
        Arrays.sort(values);
        int m = 0;
        for (int i = 0; i < sz; ++i) {
            if (i == 0 || values[i] != values[i - 1]) {
                values[m++] = values[i];
            }
        }

        int[] comp = new int[sz];
        for (int i = 0; i < sz; ++i) {
            comp[i] = modeLowerBound(values, m, a[i]);
        }

        int[] sizes = new int[m];
        for (int i = 0; i < sz; ++i) sizes[comp[i]]++;
        int[][] pos = new int[m][];
        for (int v = 0; v < m; ++v) pos[v] = new int[sizes[v]];
        int[] fill = new int[m];
        for (int i = 0; i < sz; ++i) {
            int v = comp[i];
            pos[v][fill[v]++] = i;
        }

        int B = Math.max(1, (int) Math.sqrt((double) sz));
        int nb = (sz + B - 1) / B;
        int[][] tableC = new int[nb][nb];
        int[][] tableV = new int[nb][nb];
        for (int[] row : tableV) Arrays.fill(row, -1);

        int[] cnt = new int[m];
        for (int s = 0; s < nb; ++s) {
            Arrays.fill(cnt, 0);
            int bc = 0, bv = -1;
            for (int i = s * B; i < sz; ++i) {
                int v = comp[i];
                int c = ++cnt[v];
                if (c > bc || (c == bc && v < bv)) {
                    bc = c;
                    bv = v;
                }
                if ((i + 1) % B == 0 || i == sz - 1) {
                    tableC[s][i / B] = bc;
                    tableV[s][i / B] = bv;
                }
            }
        }

        long[] answer = new long[(int) q];
        int[] cnt2 = new int[m];
        int[] touched = new int[B + 1];
        for (int t = 0; t < (int) q; ++t) {
            int l = (int) ops[t][0] - 1;
            int r = (int) ops[t][1] - 1;
            int bl = l / B, br = r / B;
            int bc, bv;
            if (bl == br) {
                bc = 0;
                bv = -1;
                int nt = 0;
                for (int i = l; i <= r; ++i) {
                    int v = comp[i];
                    if (cnt2[v] == 0) touched[nt++] = v;
                    int c = ++cnt2[v];
                    if (c > bc || (c == bc && v < bv)) {
                        bc = c;
                        bv = v;
                    }
                }
                for (int i = 0; i < nt; ++i) cnt2[touched[i]] = 0;
            } else {
                if (bl + 1 < br) {
                    bc = tableC[bl + 1][br - 1];
                    bv = tableV[bl + 1][br - 1];
                } else {
                    bc = 0;
                    bv = -1;
                }
                int end = (bl + 1) * B;
                for (int i = l; i < end; ++i) {
                    int v = comp[i];
                    int c = modeCountIn(pos[v], l, r);
                    if (c > bc || (c == bc && v < bv)) {
                        bc = c;
                        bv = v;
                    }
                }
                for (int i = br * B; i <= r; ++i) {
                    int v = comp[i];
                    int c = modeCountIn(pos[v], l, r);
                    if (c > bc || (c == bc && v < bv)) {
                        bc = c;
                        bv = v;
                    }
                }
            }
            answer[t] = values[bv];
        }
        return answer;
    }
