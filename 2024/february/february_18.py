"""
385场周赛 三题选手 给出第四题代码
巧妙运用字典树来解决前后缀匹配的问题
"""
from typing import List


class Trie:
    __slots__ = 'children', 'cnt'

    def __init__(self):
        self.children = {}
        self.cnt = 0


class Solution:
    """
    链接: https://leetcode.cn/problems/count-prefix-and-suffix-pairs-ii/description/

    描述:
    给你一个下标从 0 开始的字符串数组 words 。
    定义一个 布尔 函数 isPrefixAndSuffix ，它接受两个字符串参数 str1 和 str2 ：
    当 str1 同时是 str2 的前缀和后缀时，isPrefixAndSuffix(str1, str2) 返回 true，否则返回 false。
    例如，isPrefixAndSuffix("aba", "ababa") 返回 true，因为 "aba" 既是 "ababa" 的前缀，
    也是 "ababa" 的后缀，但是 isPrefixAndSuffix("abc", "abcd") 返回 false。
    以整数形式，返回满足 i < j 且 isPrefixAndSuffix(words[i], words[j]) 为 true 的下标对 (i, j) 的 数量 。

    示例:
    输入：words = ["a","aba","ababa","aa"]
    输出：4
    解释：在本示例中，计数的下标对包括：
    i = 0 且 j = 1 ，因为 isPrefixAndSuffix("a", "aba") 为 true 。
    i = 0 且 j = 2 ，因为 isPrefixAndSuffix("a", "ababa") 为 true 。
    i = 0 且 j = 3 ，因为 isPrefixAndSuffix("a", "aa") 为 true 。
    i = 1 且 j = 2 ，因为 isPrefixAndSuffix("aba", "ababa") 为 true 。
    因此，答案是 4 。
    """

    def countPrefixSuffixPairs(self, words: List[str]) -> int:
        # 遍历单词时候 加入其前缀和后缀的元组到字典树中 代表一个单词的信息
        # 例如遍历aba时候 加入(a, a) (b, b) (a, a) 三个元组 即zip(s, s[::-1])
        # 这样在后续遍历到其他单词时候 如果能做到匹配 那么就说明这两个单词的前缀和后缀是一样的
        # 这样我们就可以判断某个单词是不是同时是这个单词的前缀和后缀
        # 比如遍历到 ababa 时候 我们可以找到 (a, a) (b, b) (a, a) (b, b) (a, a) 五个元组
        # 这个元组的前三个正好是(a, a) (b, b) (a, a)  也就是aba这个单词插入字典书中的节点信息
        # 因为这几个元素是相同的， 所以我们可以知道aba是同时是ababa的前缀和后缀
        root = Trie()
        ans = 0
        for s in words:
            cur = root
            for p in zip(s, s[::-1]):
                if p not in cur.children:
                    cur.children[p] = Trie()

                cur = cur.children[p]
                # 之前有多少这样的单词 信息记录在cnt中
                ans += cur.cnt
            # 插入完毕在 将结尾的节点cnt加上1 代表一个单词
            cur.cnt += 1
        return ans
