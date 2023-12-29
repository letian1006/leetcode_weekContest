"""
双周赛的题目 当时打了一晚上金铲铲 头脑发昏
很简单的第四题都做不出来 在此记录一下第三题
2题选手
"""
from math import inf
from typing import List

"""
怎么枚举 
子数组分类
枚举其中一个端点 看看符合题目要求的另一个端点有多少个 可以降低复杂度
"""


class Solution:

    """
    链接：https://leetcode.cn/problems/count-the-number-of-incremovable-subarrays-ii/
    给你一个下标从 0 开始的 正 整数数组 nums 。
    如果 nums 的一个子数组满足：移除这个子数组后剩余元素 严格递增 ，
    那么我们称这个子数组为 移除递增 子数组。比方说，[5, 3, 4, 6, 7] 中的 [3, 4] 是一个移除递增子数组，
    因为移除该子数组后，[5, 3, 4, 6, 7] 变为 [5, 6, 7] ，是严格递增的。
    请你返回 nums 中 移除递增 子数组的总数目。
    注意 ，剩余元素为空的数组也视为是递增的。
    子数组 指的是一个数组中一段连续的元素序列。
    """
    def incremovableSubarrayCount(self, nums: List[int]) -> int:
        # 移除中间一段 剩下的是严格递增的 问这样的数组有多少个
        # 先算最长的严格递增前缀
        n = len(nums)
        i = 0
        while i < n - 1 and nums[i] < nums[i + 1]:
            i += 1
        # 整段数组都是递增的 所以移除任何子数组都是符合要求的
        if i == n - 1:
            return n * (n + 1) // 2
        ans = i + 2  # 此时代表为n-1为移除右端点的子数组 有多少个应该可以移除
        j = n - 1  # 表示j-1作为移除子数组的右端点
        # O(n)的做法
        tail = inf
        while j > 0 and nums[j] < tail:
            while i > -1 and nums[i] >= nums[j]:
                i -= 1
            ans += i + 2
            tail = nums[j]
            j -= 1
        return ans
