"""
五月五号的周赛 3题目选手 rank241
给出t4的做法 是一个单峰函数使用二分求极值的问题
"""
from bisect import bisect_left
from math import inf
from typing import List

MOD = 10 ** 9 + 7


class Solution:

    """
    链接: https://leetcode.cn/problems/minimum-cost-to-equalize-array/description/
    描述:
    给你一个整数数组 nums 和两个整数 cost1 和 cost2 。你可以执行以下 任一 操作 任意 次：
    从 nums 中选择下标 i 并且将 nums[i] 增加 1 ，开销为 cost1。
    选择 nums 中两个 不同 下标 i 和 j ，并且将 nums[i] 和 nums[j] 都 增加 1 ，开销为 cost2 。
    你的目标是使数组中所有元素都 相等 ，请你返回需要的 最小开销 之和。
    由于答案可能会很大，请你将它对 1e9 + 7 取余 后返回。
    示例:
    输入：nums = [4,1], cost1 = 5, cost2 = 2
    输出：15
    解释：
    执行以下操作可以使数组中所有元素相等：
    将 nums[1] 增加 1 ，开销为 5 ，nums 变为 [4,2] 。
    将 nums[1] 增加 1 ，开销为 5 ，nums 变为 [4,3] 。
    将 nums[1] 增加 1 ，开销为 5 ，nums 变为 [4,4] 。
    总开销为 15 。
    """
    def minCostToEqualizeArray(self, nums: List[int], cost1: int, cost2: int) -> int:
        n = len(nums)
        mx, mi = max(nums), min(nums)
        s = sum(nums)
        if n <= 2:
            return ((mx - mi) * cost1) % MOD  # 数组元素数量小于三个 此时只能使用操作一
        if 2 * cost1 <= cost2:
            return (mx * n - s) * cost1 % MOD  # 只用操作一
        ans = inf

        # 当操作后数组的最大值是x时候 需要付出的代价函数 定义为f 这是一个单峰函数 我们可以通过二分的方式找到最低点
        def f(x):
            need = x * n - s
            d = x - mi  # 数组中最小的数需要的增加次数
            # 贪心策略
            # 抽象为如下模型 每个盒子里有x - nums[i]个小球 每次从两个不同的盒子里面取出小球 最多能够操作多少次(也就是能够尽量多地执行操作2的次数是多少)
            # 剩下的就用操作1 规则就是这个拥有最多小球的盒子 它的数量不能超过剩下的所有盒子的小球之和 这样就可以完全使用操作2
            if d <= need - d:
                cur_cost = (need // 2) * cost2 + (need % 2) * cost1  # 可以完全使用操作2 取出所有的小球 根据need的奇偶性来看看是不是剩下最后一个小球只能使用操作1
            else:
                rest = need - d  # 第一个盒子里面的小球太多了 我们只能先把其他盒子的小球拿出来
                cur_cost = rest * cost2 + (need - 2 * rest) * cost1
            return cur_cost

        # 保证mx是偶数 能够使得二分的范围
        if mx % 2:
            # 如果mx是奇数 直接先计算最大值是mx时候应该付出的代价 然后将mx加1 继续枚举mx的其他数
            ans = f(mx)
            mx += 1


        #  这里枚举的是偶数 从mx // 2开始枚举 找到第一个使得f(x) < f(x+1)的数字
        k0 = bisect_left(range(mx), True, lo=mx // 2, key=lambda m: f(2 * m) < f(2 * (m + 1)))
        #  这里枚举的是奇数 从mx // 2开始枚举 找到第一个使得f(x) < f(x+1)的数字
        k1 = bisect_left(range(mx), True, lo=mx // 2, key=lambda m: f(2 * m + 1) < f(2 * (m + 1) + 1))
        return min(ans, f(k0 * 2), f(k1 * 2 + 1)) % MOD  # 输出最小代价
