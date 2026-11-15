#include <bits/stdc++.h>
using namespace std;

namespace {

// ---------------------------------------------------------------------------
// 状态位掩码。只有“出现不止一次、以后还可能再用”的词才占据一位（位数上界是
// 匹配边数的一半，不超过 (|verse| * 最大词长) / 2 ≤ 2000，这里给 2048 位）。
// 用定长数组实现，并提供严格弱序以便直接作为 map 的键。
constexpr int kMaskWords = 32;
using Mask = array<uint64_t, kMaskWords>;

struct MaskLess {
    bool operator()(const Mask& left, const Mask& right) const {
        for (int i = kMaskWords - 1; i >= 0; --i) {
            if (left[i] != right[i]) return left[i] < right[i];
        }
        return false;
    }
};

bool intersects(const Mask& left, const Mask& right) {
    for (int i = 0; i < kMaskWords; ++i) {
        if ((left[i] & right[i]) != 0) return true;
    }
    return false;
}

Mask unite(const Mask& left, const Mask& right) {
    Mask result{};
    for (int i = 0; i < kMaskWords; ++i) result[i] = left[i] | right[i];
    return result;
}

Mask intersect(const Mask& left, const Mask& right) {
    Mask result{};
    for (int i = 0; i < kMaskWords; ++i) result[i] = left[i] & right[i];
    return result;
}

// 把 UTF-8 字符串切到汉字边界上：返回每个字（码位）的字节起点，末尾补总长度。
vector<size_t> charBoundaries(const string& text) {
    vector<size_t> offsets;
    size_t index = 0;
    while (index < text.size()) {
        offsets.push_back(index);
        const unsigned char lead = static_cast<unsigned char>(text[index]);
        if (lead >= 0xF0) {
            index += 4;
        } else if (lead >= 0xE0) {
            index += 3;
        } else if (lead >= 0xC0) {
            index += 2;
        } else {
            index += 1;
        }
    }
    offsets.push_back(text.size());
    return offsets;
}

struct WordMatch {
    int end;     // 词结束处的字下标（左闭右开）
    int wordId;  // 去重后的词编号，等于它在词表中首次出现的顺序
};

struct Graph {
    int length = 0;                        // 诗句字数
    vector<string> words;                  // 去重后的词
    vector<vector<WordMatch>> edges;       // 顶点是汉字边界；边是一个词
    vector<Mask> wordBits;                 // 每个词占的位（只出现一次的词为 0）
    vector<Mask> futureBits;               // 从该位置起还会出现的词的位集合
};

// 建图：只保留能继续走到诗句末尾的匹配，并把同一位置的匹配按词表首次出现
// 顺序排好（这样枚举出的解的顺序和标准答案一致）。
Graph buildGraph(const string& verse, const vector<string>& dictionary) {
    Graph graph;
    const vector<size_t> offsets = charBoundaries(verse);
    const int length = static_cast<int>(offsets.size()) - 1;
    graph.length = length;

    unordered_map<string, int> wordIndex;
    wordIndex.reserve(dictionary.size() * 2 + 16);
    int maxWordLength = 0;
    for (const string& word : dictionary) {
        // 词表里可能有空词；忽略空词，保证每条边都向前推进。
        if (word.empty()) continue;
        const int charCount = static_cast<int>(charBoundaries(word).size()) - 1;
        if (charCount > length) continue;
        const auto inserted = wordIndex.emplace(word, static_cast<int>(graph.words.size()));
        if (!inserted.second) continue;
        graph.words.push_back(word);
        maxWordLength = max(maxWordLength, charCount);
    }

    graph.edges.assign(static_cast<size_t>(length) + 1, {});
    vector<char> reachable(static_cast<size_t>(length) + 1, 0);
    reachable[length] = 1;
    for (int start = length - 1; start >= 0; --start) {
        for (int len = 1; len <= maxWordLength && start + len <= length; ++len) {
            const size_t begin = offsets[start];
            const string candidate = verse.substr(begin, offsets[start + len] - begin);
            const auto found = wordIndex.find(candidate);
            if (found == wordIndex.end()) continue;
            if (!reachable[start + len]) continue;
            graph.edges[start].push_back(WordMatch{start + len, found->second});
            reachable[start] = 1;
        }
    }
    for (auto& matches : graph.edges) {
        stable_sort(matches.begin(), matches.end(),
                    [](const WordMatch& left, const WordMatch& right) { return left.wordId < right.wordId; });
    }

    const int wordCount = static_cast<int>(graph.words.size());
    vector<int> occurrences(static_cast<size_t>(wordCount), 0);
    for (const auto& matches : graph.edges) {
        for (const WordMatch& match : matches) ++occurrences[match.wordId];
    }
    graph.wordBits.assign(static_cast<size_t>(wordCount), Mask{});
    int bitIndex = 0;
    for (int wordId = 0; wordId < wordCount; ++wordId) {
        // 只出现一次的词不可能复用，无需占据集合状态的一位。
        if (occurrences[wordId] > 1) {
            graph.wordBits[wordId][bitIndex >> 6] = 1ULL << (bitIndex & 63);
            ++bitIndex;
        }
    }

    graph.futureBits.assign(static_cast<size_t>(length) + 1, Mask{});
    for (int index = length - 1; index >= 0; --index) {
        Mask mask = graph.futureBits[index + 1];
        for (const WordMatch& match : graph.edges[index]) {
            mask = unite(mask, graph.wordBits[match.wordId]);
        }
        graph.futureBits[index] = mask;
    }
    return graph;
}

// 先记忆化求出“后缀最少还需引入多少个词”，再按同样代价恢复所有最优拆分。
class VerseSolver {
public:
    explicit VerseSolver(Graph graph) : graph_(std::move(graph)) {
        memo_.resize(static_cast<size_t>(graph_.length) + 1);
        path_.assign(static_cast<size_t>(graph_.length), string());
    }

    vector<string> run() {
        if (graph_.edges[0].empty()) return {};
        collect(0, Mask{}, 0);
        return answers_;
    }

private:
    // used 只记录“以前用过、以后仍可能出现”的词；返回后缀最少还需引入的词数。
    int minimumCost(int index, const Mask& used) {
        if (index == graph_.length) return 0;
        auto& memo = memo_[index];
        const auto cached = memo.find(used);
        if (cached != memo.end()) return cached->second;
        int best = graph_.length + 1;
        for (const WordMatch& match : graph_.edges[index]) {
            const pair<int, Mask> next = step(match, used);
            const int cost = next.first + minimumCost(match.end, next.second);
            if (cost < best) {
                best = cost;
                if (best == 0) break;
            }
        }
        memo.emplace(used, best);
        return best;
    }

    void collect(int index, const Mask& used, int depth) {
        if (index == graph_.length) {
            string answer;
            for (int i = 0; i < depth; ++i) {
                if (i) answer += ' ';
                answer += path_[i];
            }
            answers_.push_back(std::move(answer));
            return;
        }
        const int best = minimumCost(index, used);
        for (const WordMatch& match : graph_.edges[index]) {
            const pair<int, Mask> next = step(match, used);
            if (next.first + minimumCost(match.end, next.second) == best) {
                path_[depth] = graph_.words[match.wordId];
                collect(match.end, next.second, depth + 1);
            }
        }
    }

    // 走这条边：返回（是否新引入了一个词，走完后应保留的状态）。
    pair<int, Mask> step(const WordMatch& match, const Mask& used) const {
        const Mask& bit = graph_.wordBits[match.wordId];
        const int extra = intersects(used, bit) ? 0 : 1;
        // 越过某个词的最后匹配位置后，该词可以安全地从状态中遗忘。
        return {extra, intersect(unite(used, bit), graph_.futureBits[match.end])};
    }

    Graph graph_;
    vector<map<Mask, int, MaskLess>> memo_;
    vector<string> path_;
    vector<string> answers_;
};

}  // namespace

vector<string> solve(const string& verse, const vector<string>& words) {
    if (verse.empty()) return {};
    VerseSolver solver(buildGraph(verse, words));
    return solver.run();
}
