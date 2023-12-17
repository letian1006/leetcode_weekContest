from itertools import accumulate

from typing import List
"""
12-17日的周赛
链接:https://leetcode.cn/contest/weekly-contest-376/
"""
class Solution:
    # 链接:https://leetcode.cn/problems/apply-operations-to-maximize-frequency-score/description/
    def maxFrequencyScore(self, nums: List[int], k: int) -> int:
        """
        给你一个下标从 0 开始的整数数组 nums 和一个整数 k
        你可以对数组执行 至多 k 次操作：
        从数组中选择一个下标 i ，将 nums[i] 增加 或者 减少 1 。
        最终数组的频率分数定义为数组中众数的 频率 。
        请你返回你可以得到的 最大 频率分数。
        众数指的是数组中出现次数最多的数。一个元素的频率指的是数组中这个元素的出现次数。
        """
        # 滑动窗口 加上前缀和的思想
        nums.sort()
        s = list(accumulate(nums, initial=0))
        n = len(nums)
        l = ans = 0
        def get_dis(left: int ,right: int) -> int:
            # 将这个区间全部变成一样的数字需要的最少操作次数
            # 思想就是中位数贪心
            # 前缀和求差得到操作次数
            mid = (left + right) // 2
            left_sum = (mid - left) * nums[mid] - (s[mid] - s[left])
            right_sum = s[right+1] - s[mid + 1] - (right - mid) * nums[mid]
            return left_sum + right_sum
        for r in range(n):
            if get_dis(l, r) > k:
                l += 1
            ans = max(ans, r - l + 1)
        return ans