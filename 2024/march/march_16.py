"""
3月16号的周赛 两题选手
t3是一个脑筋急转弯 t4是一个经典的背包问题
"""
from collections import Counter
from heapq import heapify, heappop, heappush
from string import ascii_lowercase
from typing import List


class Solution:
    """
    链接: https://leetcode.cn/problems/replace-question-marks-in-string-to-minimize-its-value/
    描述:
    给你一个字符串 s 。s[i] 要么是小写英文字母，要么是问号 '?' 。
    对于长度为 m 且 只 含有小写英文字母的字符串 t ，我们定义函数 cost(i) 为下标 i 之前（也就是范围 [0, i - 1] 中）出现过与 t[i] 相同 字符出现的次数。
    字符串 t 的 分数 为所有下标 i 的 cost(i) 之 和 。
    比方说，字符串 t = "aab" ：
    cost(0) = 0
    cost(1) = 1
    cost(2) = 0
    所以，字符串 "aab" 的分数为 0 + 1 + 0 = 1 。
    你的任务是用小写英文字母 替换 s 中 所有 问号，使 s 的 分数最小 。
    请你返回替换所有问号 '?' 之后且分数最小的字符串。如果有多个字符串的 分数最小 ，那么返回字典序最小的一个。
    示例:
    输入：s = "???"
    输出： "abc"
    解释：这个例子中，我们将 s 中的问号 '?' 替换得到 "abc" 。
    对于字符串 "abc" ，cost(0) = 0 ，cost(1) = 0 和 cost(2) = 0 。
    "abc" 的分数为 0 。
    其他修改 s 得到分数 0 的字符串为 "cba" ，"abz" 和 "hey" 。
    这些字符串中，我们返回字典序最小的
    """

    def minimizeStringValue(self, s: str) -> str:
        # 我们发现一个问题 也就是整个字符串s的分数 只取决于每个字符的频率
        # 比如 有三个a 这些a的排列位置是不影响a对整个字符串贡献的分数的
        # 因此我们可以得到一个贪心的策略 也就是对?处的字符使用频率最小的字符来替代
        cnt = Counter(s)
        heap = [(cnt[c], c) for c in ascii_lowercase]
        heapify(heap)
        ans = []
        for c in s:
            if c == '?':
                # 找到当前频率最小的字符 替换当前的问号
                count, cur = heappop(heap)
                ans.append(cur)
                heappush(heap, (count + 1, cur))
        ans.sort()  # 这里排序是为了获得字典序最小的字符
        j = 0
        s = list(s)
        for i, c in enumerate(s):
            # 替换问号 但是不替换其他字符
            if c == '?':
                s[i] = ans[j]
                j += 1
        return ''.join(s)

    """
    链接: https://leetcode.cn/problems/find-the-sum-of-the-power-of-all-subsequences/
    描述:
    给你一个长度为 n 的整数数组 nums 和一个 正 整数 k 。
    一个整数数组的 能量 定义为和 等于 k 的子序列的数目。
    请你返回 nums 中所有子序列的 能量和 。
    由于答案可能很大，请你将它对 109 + 7 取余 后返回。
    示例:
    输入：  nums = [1,2,3], k = 3 
    输出：  6 
    就是下面的 1; 2; 3; 1,2; 1,3; 2,3; 1,2,3 所有的子序列 针对上述的每一个子序列 有多少个和为k的子序列
    比如3 有一个子序列的和为3 
    1,2,3 有两个子序列的和为3 即1,2 和 3
    1,2 有一个子序列的和为3 即1,2
    2,3 有一个子序列的和为3 即3
    1,3 有一个子序列的和为3 即3
    一共有6个子序列的和为3 因此答案是6
    """
    def sumOfPower(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        # 子序列的和为k的子序列的数目 经典的0-1背包问题
        f = [0] * (k + 1)  # f[i][j]表示前i个数中和为j的子序列的数目 我将第一个维度优化掉了
        f[0] = 1  # 一个数都不选的时候和为0的子序列有1个
        for c in nums:
            for j in range(k, -1, -1):
                if j >= c:
                    # 选或者不选当前的数 如果不选当前的数 那么
                    f[j] = (f[j - c] + f[j] * 2) % MOD
                else:
                    # 如果当前的数比j大 只能不选当前的数字
                    # 这里为什么要乘2呢 考虑到新添加的数字c带来的影响
                    # 他会产生一系列新的子序列，这些子序列可以不包含当前的数字 
                    # 你可以把之前的子序列的和为j的子序列当成不包含c的子序列 也就是多加了一份
                    # 所以要乘上2
                    f[j] = f[j] * 2 % MOD
        return f[-1]
