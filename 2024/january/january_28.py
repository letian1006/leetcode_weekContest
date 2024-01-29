"""
2024-1-29的周赛
三题选手 最后一题的难度分估计在2900
周赛链接:https://leetcode.cn/contest/weekly-contest-382/
"""
from typing import List

"""
位运算的两个技巧
1、拆位 每个bit位单独考虑
2、

相邻操作 即子数组的合并
"""


class Solution:
    """
    题目链接:https://leetcode.cn/problems/minimize-or-of-remaining-elements-using-operations/description/
    题目描述：
    给你一个下标从 0 开始的整数数组 nums 和一个整数 k 。
    一次操作中，你可以选择 nums 中满足 0 <= i < nums.length - 1 的一个下标 i ，
    并将 nums[i] 和 nums[i + 1] 替换为数字 nums[i] & nums[i + 1] ，其中 & 表示按位 AND 操作。
    请你返回 至多 k 次操作以内，使 nums 中所有剩余元素按位 OR 结果的 最小值
    
    示例：
    输入：nums = [3,5,3,2,7], k = 2
    输出：3
    解释：执行以下操作：
    1. 将 nums[0] 和 nums[1] 替换为 (nums[0] & nums[1]) ，得到 nums 为 [1,3,2,7] 。
    2. 将 nums[2] 和 nums[3] 替换为 (nums[2] & nums[3]) ，得到 nums 为 [1,3,2] 。
    最终数组的按位或值为 3 。
    3 是 k 次操作以内，可以得到的剩余元素的最小按位或值。
    """

    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        ans = mask = 0
        # 从高位到低位的贪心 看看这一位能不能构造成0
        # 如果不能这一位就需要被置成1 并在之后的位置上不再考虑这一位的
        # 如果可以构造得到0 那么后面在观察低位能不能构造成0的时候 需要保证高位不能构造成1 也就是需要考虑
        # 如最高位为 1 0 1 0 1 0看看这个最高位能不能通过相邻的and运算变成全0 那么我们进行子数组的合并 看看需要多少次操作才可以做到
        # 首先初始化结果为-1 表示全1 然后逐渐挨个and
        for i in range(29, -1, -1):
            # 首先通过mask将需要考虑的位置全部提取出来 我们在遍历到第i个比特位时 不仅需要保证这一位能够变成0
            # 还要考虑之前的可以变成0的高位不能变成1 对于哪些无论如何都是1的位置 我们就不再考虑 通过mask盖掉(置成0)
            
            mask |= 1 << i
            cur = -1
            cnt = 0
            for n in nums:
                cur &= mask & n
                # 如果and的结果不是0 那么我们就需要多引入前面一段的0 也就是这一段要全部变成0 需要的合并次数是这一段的长度
                # 如果and的结果是0 那么这一段全部变成0需要的合并次数就是len(这一段的长度) - 1
                # 体现在代码上就是cur不是0就cnt + 1变成0的时候 重制cur为-1 合并下一段
                if cur:
                    cnt += 1
                else:
                    cur = -1
            if cnt > k:
                # 如果将这一段全部变成0的操作次数超过了k 那么这一段就不能变成0 也就是这一位一定是1
                # 那么我们在接着考虑后面的低位时候 就不再考虑这一位 也就是通过mask将这一位去掉 不再考虑
                # 体现在代码上就是mask ^= 1 << i
                ans |= 1 << i
                mask ^= 1 << i
        return ans
