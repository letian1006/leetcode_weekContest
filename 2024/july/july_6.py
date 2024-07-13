"""
双周赛的最后一题 没有做出来的log trick
链接: https://leetcode.cn/problems/number-of-subarrays-with-and-value-of-k/description/
"""
from typing import List

class Solution:
    """
    链接: https://leetcode.cn/problems/number-of-subarrays-with-and-value-of-k/description/
    描述: 
    给你一个整数数组 nums 和一个整数 k ，请你返回 nums 中有多少个子数组
    满足：子数组中所有元素按位 AND 的结果为 k 。
    示例:
    输入: nums = [1,1,2], k = 1
    输出: 3
    解释: 按位 AND 值为 1 的子数组包括：[1,1,2], [1,1,2], [1,1,2] 。
    思路: 整体思路还是使用and运算的性质 本质上是求交集 选择一个数字作为子数组右端点 往左边扩展
    and运算的结果是不会变小的 将and的结果保存下来 如果下一个数字和and的结果相等 那么这个数字是and的子集
    那么这个数字左边的所有数字都是and的子集 因此不用更新 直接break
    为了遍历过程中找到有多少ige子数组and的结果等于k 我们使用两个指针left和right
    left指针找到第一个小于等于k的数字的下标 right指针找到第一个大于k的数字的下标
    因为and运算的性质 因此我们遍历到i位置的时候nums[:i+1]是一个单调不减的数组 
    因此有多少个子数组的and结果等于k就是right - left计算得到
    """
    def countSubarrays(self, nums: List[int], k: int) -> int:
        ans = left = right = 0
        for i, x in enumerate(nums):
            
            for j in range(i - 1, -1, -1):
                # 精髓就在这里 如果nums[j] & x == nums[j]证明nums[j]是x的子集
                # 那么之前的所有子数组都是x的子集 如果继续使用&来更新 前面的数字是不会变化的所以可以直接退出
                if nums[j] & x == nums[j]:
                    break
                nums[j] &= x
                x = nums[j]
            # 找出两个边界 第一个边界是nums[left] <= k的下标
            while left <= i and nums[left] < k:
                left += 1
            while right <= i and nums[right] <= k:
                right += 1
            ans += right - left
            
        return ans

