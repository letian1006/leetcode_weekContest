"""
2024-2-4的周赛
三题选手
最后一题给出z函数的模版和定义
"""


class Solution:
    """
    链接: https://leetcode.cn/problems/minimum-time-to-revert-word-to-initial-state-ii/

    描述:
    给你一个下标从 0 开始的字符串 word 和一个整数 k 。
    在每一秒，你必须执行以下操作：
    移除 word 的前 k 个字符。
    在 word 的末尾添加 k 个任意字符。
    注意 添加的字符不必和移除的字符相同。但是，必须在每一秒钟都执行 两种 操作。
    返回将 word 恢复到其 初始 状态所需的 最短 时间（该时间必须大于零）。

    示例:
    输入：word = "abacaba", k = 3
    输出：2
    解释：
    第 1 秒，移除 word 的前缀 "aba"，并在末尾添加 "bac" 。因此，word 变为 "cababac"。
    第 2 秒，移除 word 的前缀 "cab"，并在末尾添加 "aba" 。因此，word 变为 "abacaba" 并恢复到始状态。
    可以证明，2 秒是 word 恢复到其初始状态所需的最短时间。
    """

    def minimumTimeToInitialState(self, word: str, k: int) -> int:
        #  就是看移除n * k个字符后 剩下的字符串能不能成为原字符串的前缀 只要是原来字符串的前缀即可
        #  因此我们使用z函数
        #  z函数的定义:是一个字符串的z函数是一个数组，z[i]表示以i为起点的字符串和原字符串的最长公共前缀
        n = len(word)
        z = [0] * n
        l, r = 0, 0
        for i in range(1, n):
            if i <= r:
                # 在z-box内部 取两者的最小值 第一个是i到r的长度 第二个是z[i - l]的长度
                # i - l是i在z-box中的相对位置
                z[i] = min(r - i + 1, z[i - l])
            while i + z[i] < n and word[z[i]] == word[i + z[i]]:
                l, r = i, i + z[i]
                z[i] += 1
            if i % k == 0 and z[i] == n - i:
                return i // k
        return (n + k - 1) // k
