"""
双周赛的最后一道题 2024.6.22
"""
from typing import List

MOD = 10 ** 9 + 7


class Solution:
    """
    链接:https://leetcode.cn/problems/count-the-number-of-inversions/description/
    描述:
    给你一个整数 n 和一个二维数组 requirements ，其中 requirements[i] = [endi, cnti]
    表示这个要求中的末尾下标和 逆序对 的数目。
    整数数组 nums 中一个下标对 (i, j) 如果满足以下条件，那么它们被称为一个 逆序对 ：
    i < j 且 nums[i] > nums[j]
    请你返回 [0, 1, 2, ..., n - 1] 的
    排列 perm 的数目，满足对 所有 的 requirements[i] 都有 perm[0..endi] 恰好有 cnti 个逆序对
    由于答案可能会很大，将它对 1e9 + 7 取余 后返回。
    示例:
    输入：n = 3, requirements = [[2,2],[0,0]]
    输出：2
    解释：
    两个排列为：
    [2, 0, 1]
    前缀 [2, 0, 1] 的逆序对为 (0, 1) 和 (0, 2) 。
    前缀 [2] 的逆序对数目为 0 个。
    [1, 2, 0]
    前缀 [1, 2, 0] 的逆序对为 (0, 2) 和 (1, 2) 。
    前缀 [1] 的逆序对数目为 0 个。
    """

    def numberOfPermutations(self, n: int, requirements: List[List[int]]) -> int:
        """
        解释 定义dp状态dp[i][j]为前i个数字 能够形成j个逆序对的排列方案数目
        """
        need = [-1] * n  # 表示当前下标的逆序对数目 也就是题目的要求
        need[0] = 0
        for end, cnt in requirements:
            need[end] = cnt
        if need[0]:
            return 0
        mx = max(need)
        # 定义dp数组
        dp = [[0] * (mx + 1) for _ in range(n)]  # dp[i][j]表示前i个数中逆序对数目为j的排列数目
        dp[0][0] = 1
        for i in range(1, n):
            m = mx if need[i] == -1 else need[i]  # 可以产生的逆序对的最大值 如果need[i]为-1 表示这个位置上没有约束 否则有约束 此时我们只需要枚举j到need[i]即可
            r = need[i - 1]  # 前面一个数字的逆序对是多少 如果是-1就没有要求 否则前一个位置的逆序对数目就必须是r
            if r >= 0:  # 前一个位置上的逆序对必须是r
                for j in range(r, min(i + r, m) + 1):  # j不能太小 至少能够满足上一个位置要求的逆序对数目r
                    # 当然也不能太大 当前i位置最多能够产生i个逆序对 加上前面的r个逆序对 我们此时最多产生i+r个逆序对 再与此时的限制m取最小值即可
                    dp[i][j] = dp[i - 1][r]
            else:
                # 没有限制的话 我们可以枚举此时i位置上的逆序对数目 从0到最大值m
                for j in range(m + 1):
                    # 枚举此时i位置上的逆序对数目
                    dp[i][j] = sum(dp[i - 1][j - k] for k in range(min(i, j) + 1)) % MOD

        return dp[-1][need[-1]]
