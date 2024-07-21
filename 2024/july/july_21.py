"""
核心就是一个 从nums到target之间有差异
因此我们使target[i] - nums[i]得到一个数组a[i]
这个数组就是我们希望通过题目的操作生成的 这个操作可以等价为两个差分数组的两个端点的操作
最后通过对这个差分数组求前缀和就得到了a 
反过来最关键的就是通过a前后项求差得到原来的差分数组 这个差分数组按照贪心的规则就可以使用最少的操作次数得到
"""
from typing import List
from itertools import pairwise


class Solution:
    """
    链接: https://leetcode.cn/problems/minimum-operations-to-make-array-equal-to-target/description/
    描述: 
    给你两个长度相同的正整数数组 nums 和 target。在一次操作中，你可以选择 nums 的任何子数组
    ，并将该子数组内的每个元素的值增加或减少 1。

    返回使 nums 数组变为 target 数组所需的 最少 操作次数。
    示例:
    输入： nums = [3,5,1,2], target = [4,6,2,4]
    输出： 2
    解释：
    执行以下操作可以使 nums 等于 target：
    - nums[0..3] 增加 1，nums = [4,6,2,3]。
    - nums[3..3] 增加 1，nums = [4,6,2,4]。
    """
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        s = target[0] - nums[0]
        ans = abs(s)
        # 我们从target - nums得到两者之间的差值 这就是我们需要通过操作生成的数组
        # 设其为a 则nums + a就可以得到原数组 原来的操作可以看成差分数组两个端点的操作
        for (a, b), (c, d) in pairwise(zip(target, nums)):
            diff = (c - d) - (a - b) # a数组的前后两项的差值 也就是差分数组这个位置上的数值
            # s大于0 代表之前累积的操作的结果是+1 操作 也就是说后面有s次免费次数的-1操作可以使用
            # s小于0 代表之前累积的操作的结果是-1操作 后面有abs(s)次免费次数的+1操作可以使用
            if s >= 0 and diff >= 0:
                ans += diff
                s += diff
            elif s >= 0 and diff < 0:
                # s是正数 则代表此时我们有免费的-1操作可以在此刻使用
                if s >= -diff:
                    s += diff
                else:
                    ans += abs(s + diff)
                    s = s + diff
            elif s <= 0 and diff >= 0:
                if diff <= -s:
                    s += diff
                else:
                    ans += abs(diff + s)
                    s = diff + s
            else:
                ans += abs(diff)
                s += diff
        return ans