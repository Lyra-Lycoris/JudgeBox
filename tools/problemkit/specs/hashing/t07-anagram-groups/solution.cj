package t07_anagram_groups

import std.collection.*
import std.sort.*

func solve(n: Int64, words: Array<String>): Int64 {
    let groups = HashSet<String>()
    for (word in words) {
        let letters = word.toRuneArray()
        sort(letters)
        let builder = StringBuilder()
        for (ch in letters) {
            builder.append(ch.toString())
        }
        groups.add(builder.toString())
    }
    return Int64(groups.size)
}
