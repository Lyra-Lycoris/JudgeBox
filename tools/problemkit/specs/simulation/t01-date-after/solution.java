    static boolean isLeapYear(long year) {
        return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
    }

    static long daysBeforeYear(long year) {
        long t = year - 1;
        return t * 365 + t / 4 - t / 100 + t / 400;
    }

    static long dayOfYear(long year, long month, long day) {
        long[] cum = {0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334};
        long value = cum[(int) month] + day - 1;
        if (month > 2 && isLeapYear(year)) value += 1;
        return value;
    }

    static long daysInMonth(long year, long month) {
        if (month == 2) return isLeapYear(year) ? 29 : 28;
        if (month == 4 || month == 6 || month == 9 || month == 11) return 30;
        return 31;
    }

    static String solve(long y, long m, long d, long k) {
        long total = daysBeforeYear(y) + dayOfYear(y, m, d) + k;
        long lo = 1, hi = 1 + total / 365 + 2;
        while (lo < hi) {
            long mid = (lo + hi + 1) / 2;
            if (daysBeforeYear(mid) <= total) lo = mid; else hi = mid - 1;
        }
        long year = lo;
        long doy = total - daysBeforeYear(year);
        long month = 1;
        while (true) {
            long length = daysInMonth(year, month);
            if (doy < length) break;
            doy -= length;
            month += 1;
        }
        return String.format("%04d-%02d-%02d", year, month, doy + 1);
    }
