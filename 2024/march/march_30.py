"""
127场双周赛
链接:https://leetcode.cn/contest/biweekly-contest-127/
三题选手 t3使用了一个二分卡线过 下面给出t3优化后的代码
以及没有做出的t4代码

"""
from functools import cache
from math import inf
from typing import List

"""
或值套路题目
"""
MOD = 10 ** 9 + 7


class Solution:
    """
    描述:
    给你一个 非负 整数数组 nums 和一个整数 key 。
    如果一个数组中所有元素的按位或运算 OR 的值 至少 为 key ，那么我们称这个数组是 特别的 。
    请你返回 nums 中 最短特别非空子数组
    的长度，如果特别子数组不存在，那么返回 -1 。
    链接:https://leetcode.cn/problems/shortest-subarray-with-or-at-least-k-ii/description/
    示例:
    输入：nums = [1,2,3], k = 2
    输出：1
    解释：子数组 [3] 的按位 OR 值为 3 ，所以我们返回 1
    """

    def minimumSubarrayLength(self, nums: List[int], key: int) -> int:
        ans = inf
        # 第一次或值出现的位置 越往右越好
        m = {}
        for i, c in enumerate(nums):
            # 越或越大 m中保存的是之前出现的或值 就是从nums[0] 到nums[i-1]能出现的所有或值
            # 然后保存最左边那个或值 使其出现的子数组最短
            # 由于或运算的性质 m中最多只有32个元素
            m = {k | c: v for k, v in m.items()}
            m[c] = i
            for k, v in m.items():
                # v是最左侧
                if k >= key:
                    ans = min(ans, i - v + 1)
        return ans if ans < inf else -1

    """
    描述:
    给你一个长度为 n 的整数数组 nums 和一个 正 整数 k 。
    一个子序列的 能量 定义为子序列中 任意 两个元素的差值绝对值的 最小值 。
    请你返回 nums 中长度 等于 k 的 所有 子序列的 能量和 。
    由于答案可能会很大，将答案对 10^9 + 7 取余 后返回
    链接:https://leetcode.cn/problems/find-the-sum-of-subsequence-powers/description/
    示例:
    输入：nums = [1,2,3,4], k = 3
    输出：4
    解释：
    nums 中总共有 4 个长度为 3 的子序列：[1,2,3] ，[1,3,4] ，[1,2,4] 和 [2,3,4] 。
    能量和为 |2 - 3| + |3 - 4| + |2 - 1| + |3 - 4| = 4 。
    """

    def sumOfPowers(self, nums: List[int], k: int) -> int:
        # 子序列dp题目 前后两项相关因此 因此需要带上上一个数字的信息
        # 然后硬cache 记忆化搜索
        nums.sort()

        @cache
        def dfs(i, rest, pre, min_diff):
            # 当前位置 还有多少个数要填 pre是上一个数 min_diff是当前的最小差值
            if rest > i + 1:
                return 0
            if rest == 0:
                return min_diff
            res1 = dfs(i - 1, rest, pre, min_diff)
            res2 = dfs(i - 1, rest - 1, nums[i], min(min_diff, pre - nums[i]))
            return (res1 + res2) % MOD

        # 直接暴力计算得分 即可
        ans = dfs(len(nums) - 1, k, inf, inf)
        dfs.cache_clear()
        return ans
