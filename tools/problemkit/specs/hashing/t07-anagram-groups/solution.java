    static long solve(long n, String[] words) {
        Set<String> groups = new HashSet<>();
        for (String word : words) {
            char[] letters = word.toCharArray();
            Arrays.sort(letters);
            groups.add(new String(letters));
        }
        return groups.size();
    }
