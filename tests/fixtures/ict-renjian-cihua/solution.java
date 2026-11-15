    static List<String> solve(String verse, String[] words) {
        if (verse.isEmpty()) return new ArrayList<>();
        return new VerseSolver(buildGraph(verse, words)).run();
    }

    static final class WordMatch {
        final int end;     // 词结束处的字下标（左闭右开）
        final int wordId;  // 去重后的词编号，等于它在词表中首次出现的顺序

        WordMatch(int end, int wordId) {
            this.end = end;
            this.wordId = wordId;
        }
    }

    static final class Graph {
        int length;                              // 诗句字数
        final List<String> words = new ArrayList<>();          // 去重后的词
        final List<List<WordMatch>> edges = new ArrayList<>(); // 顶点是汉字边界；边是一个词
        final List<BigInteger> wordBits = new ArrayList<>();   // 每个词占的位（只出现一次的词为 0）
        final List<BigInteger> futureBits = new ArrayList<>(); // 从该位置起还会出现的词的位集合
    }

    // 建图：只保留能继续走到诗句末尾的匹配，并把同一位置的匹配按词表首次出现
    // 顺序排好（这样枚举出的解的顺序和标准答案一致）。
    static Graph buildGraph(String verse, String[] dictionary) {
        int[] text = verse.codePoints().toArray();
        Graph graph = new Graph();
        graph.length = text.length;

        Map<String, Integer> wordIndex = new HashMap<>();
        int maxWordLength = 0;
        for (String word : dictionary) {
            // 词表里可能有空词；忽略空词，保证每条边都向前推进。
            if (word.isEmpty()) continue;
            int length = word.codePointCount(0, word.length());
            if (length > text.length) continue;
            if (wordIndex.containsKey(word)) continue;
            wordIndex.put(word, graph.words.size());
            graph.words.add(word);
            maxWordLength = Math.max(maxWordLength, length);
        }

        for (int i = 0; i <= text.length; ++i) graph.edges.add(new ArrayList<>());
        boolean[] reachable = new boolean[text.length + 1];
        reachable[text.length] = true;
        for (int start = text.length - 1; start >= 0; --start) {
            for (int length = 1; length <= maxWordLength && start + length <= text.length; ++length) {
                Integer wordId = wordIndex.get(new String(text, start, length));
                if (wordId == null || !reachable[start + length]) continue;
                graph.edges.get(start).add(new WordMatch(start + length, wordId));
                reachable[start] = true;
            }
        }
        for (List<WordMatch> matches : graph.edges) {
            matches.sort(Comparator.comparingInt((WordMatch match) -> match.wordId));
        }

        int wordCount = graph.words.size();
        int[] occurrences = new int[wordCount];
        for (List<WordMatch> matches : graph.edges) {
            for (WordMatch match : matches) ++occurrences[match.wordId];
        }
        int bitIndex = 0;
        for (int wordId = 0; wordId < wordCount; ++wordId) {
            // 只出现一次的词不可能复用，无需占据集合状态的一位。
            if (occurrences[wordId] > 1) {
                graph.wordBits.add(BigInteger.ONE.shiftLeft(bitIndex));
                ++bitIndex;
            } else {
                graph.wordBits.add(BigInteger.ZERO);
            }
        }

        for (int i = 0; i <= text.length; ++i) graph.futureBits.add(BigInteger.ZERO);
        for (int index = text.length - 1; index >= 0; --index) {
            BigInteger mask = graph.futureBits.get(index + 1);
            for (WordMatch match : graph.edges.get(index)) {
                mask = mask.or(graph.wordBits.get(match.wordId));
            }
            graph.futureBits.set(index, mask);
        }
        return graph;
    }

    // 先记忆化求出“后缀最少还需引入多少个词”，再按同样代价恢复所有最优拆分。
    static final class VerseSolver {
        private final Graph graph;
        private final List<Map<BigInteger, Integer>> memo = new ArrayList<>();
        private final String[] path;
        private final List<String> answers = new ArrayList<>();

        VerseSolver(Graph graph) {
            this.graph = graph;
            this.path = new String[graph.length];
            for (int i = 0; i <= graph.length; ++i) memo.add(new HashMap<>());
        }

        List<String> run() {
            if (graph.edges.get(0).isEmpty()) return new ArrayList<>();
            collect(0, BigInteger.ZERO, 0);
            return answers;
        }

        // used 只记录“以前用过、以后仍可能出现”的词；返回后缀最少还需引入的词数。
        private int minimumCost(int index, BigInteger used) {
            if (index == graph.length) return 0;
            Map<BigInteger, Integer> cache = memo.get(index);
            Integer cached = cache.get(used);
            if (cached != null) return cached;
            int best = graph.length + 1;
            for (WordMatch match : graph.edges.get(index)) {
                BigInteger bit = graph.wordBits.get(match.wordId);
                int extra = used.and(bit).signum() == 0 ? 1 : 0;
                // 越过某个词的最后匹配位置后，该词可以安全地从状态中遗忘。
                BigInteger nextUsed = used.or(bit).and(graph.futureBits.get(match.end));
                int cost = extra + minimumCost(match.end, nextUsed);
                if (cost < best) {
                    best = cost;
                    if (best == 0) break;
                }
            }
            cache.put(used, best);
            return best;
        }

        private void collect(int index, BigInteger used, int depth) {
            if (index == graph.length) {
                StringBuilder answer = new StringBuilder();
                for (int i = 0; i < depth; ++i) {
                    if (i > 0) answer.append(' ');
                    answer.append(path[i]);
                }
                answers.add(answer.toString());
                return;
            }
            int best = minimumCost(index, used);
            for (WordMatch match : graph.edges.get(index)) {
                BigInteger bit = graph.wordBits.get(match.wordId);
                int extra = used.and(bit).signum() == 0 ? 1 : 0;
                BigInteger nextUsed = used.or(bit).and(graph.futureBits.get(match.end));
                if (extra + minimumCost(match.end, nextUsed) == best) {
                    path[depth] = graph.words.get(match.wordId);
                    collect(match.end, nextUsed, depth + 1);
                }
            }
        }
    }
