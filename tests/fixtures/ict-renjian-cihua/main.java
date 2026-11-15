    public static void main(String[] args) throws Exception {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String first = reader.readLine();
        if (first == null) return;
        int cases = Integer.parseInt(first.trim());
        StringBuilder output = new StringBuilder();
        for (int t = 0; t < cases; ++t) {
            String verse = reader.readLine().trim();
            int count = Integer.parseInt(reader.readLine().trim());
            String[] words = new String[count];
            for (int i = 0; i < count; ++i) words[i] = reader.readLine().trim();
            List<String> answers = solve(verse, words);
            output.append(answers.size()).append('\n');
            for (String answer : answers) output.append(answer).append('\n');
        }
        PrintWriter writer = new PrintWriter(new OutputStreamWriter(System.out, "UTF-8"));
        writer.print(output);
        writer.flush();
    }
