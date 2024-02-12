"""
2024-2-11的周赛
大年初二 第三题没有做出来 最后一题是z函数匹配的题目
我用的是字符串哈希做的 后面需要补充一下这个板子
"""

from collections import Counter
from typing import List


class Solution:
    """
    链接: https://leetcode.cn/problems/maximum-palindromes-after-operations/description/

    描述:
    给你一个下标从 0 开始的字符串数组 words ，数组的长度为 n ，且包含下标从 0 开始的若干字符串。
    你可以执行以下操作 任意 次数（包括零次）：
    选择整数i、j、x和y，满足0 <= i, j < n，0 <= x < words[i].length，0 <= y < words[j].length，交换 字符 words[i][x] 和 words[j][y] 。
    返回一个整数，表示在执行一些操作后，words 中可以包含的回文字符串的 最大 数量。
    注意：在操作过程中，i 和 j 可以相等。

    示例:
    输入：words = ["abbb","ba","aa"]
    输出：3
    解释：在这个例子中，获得最多回文字符串的一种方式是：
    选择 i = 0, j = 1, x = 0, y = 0，交换 words[0][0] 和 words[1][0] 。
    words 变成了 ["bbbb","aa","aa"] 。
    words 中的所有字符串都是回文。
    因此，可实现的回文字符串的最大数量是 3 
    """
    def maxPalindromesAfterOperations(self, words: List[str]) -> int:
        cnt = Counter()
        for w in words:
            cnt += Counter(w)
        # 奇数回文串中间一个字母填什么都可以
        # 我们这里计算的left就是能够找到另一半的字母数量
        # 后面遍历的时候 贪心地从短的字符串往长的字符串开始填
        # 遍历到的单词长度为l 我们就需要l // 2个字符
        left = sum(v // 2 for v in cnt.values())
        ans = 0
        words.sort(key=len)
        for w in words:
            l = len(w)
            if left >= l // 2:
                ans += 1
                left -= l // 2
            else:
                return ans
        return ans
