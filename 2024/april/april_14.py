"""
2024-4-14的周赛 两题选手
考虑一般的容斥原理的第三题 以及最后一个大胆一点的dp题目
"""
from functools import lru_cache
from math import lcm, inf
from typing import List


class Solution:
    """
    链接: https://leetcode.cn/problems/kth-smallest-amount-with-single-denomination-combination/description/
    描述:
    给你一个整数数组 coins 表示不同面额的硬币，另给你一个整数 k 。
    你有无限量的每种面额的硬币。但是，你 不能 组合使用不同面额的硬币。
    返回使用这些硬币能制造的 第 kth 小 金额
    示例:
    输入： coins = [3,6,9], k = 3
    输出： 9
    解释：给定的硬币可以制造以下金额：
    3元硬币产生3的倍数：3, 6, 9, 12, 15等。
    6元硬币产生6的倍数：6, 12, 18, 24等。
    9元硬币产生9的倍数：9, 18, 27, 36等。
    所有硬币合起来可以产生：3, 6, 9, 12, 15等。
    数据范围说明:
    1 <= coins.length <= 15
    1 <= coins[i] <= 25
    1 <= k <= 2 * 109
    coins 包含两两不同的整数。
    """

    def findKthSmallest(self, coins: List[int], k: int) -> int:
        # 对k进行二分
        l, r = k - 1, k * min(coins)
        ans = -1
        n = len(coins)

        def get(num):
            count = 0
            for i in range(1, 1 << n):
                lcm_res = 1  # 这个子集所代表的数 也就是选中的coins的最小公倍数
                for j, c in enumerate(coins):
                    if (i >> j) & 1:
                        lcm_res = lcm(lcm_res, c)
                    if lcm_res > num:
                        break
                # 容斥原理的核心 选中的个数是奇数个的时候加上去 选中的个数是偶数个的时候减去
                # 也就是子集包含的元素数量的奇偶性 子集合的代表即多个元素的lcm
                count += num // lcm_res if i.bit_count() % 2 else -(num // lcm_res)
            return count

        while l <= r:
            mid = l + r >> 1
            # 看看小于mid的有多少个数 只要小于mid的数的个数大于等于k就可以
            cur = get(mid)
            if cur > k:

                r = mid - 1
            elif cur < k:
                l = mid + 1
            else:
                ans = mid
                r = mid - 1
        return ans

    def minimumValueSum(self, nums: List[int], andValues: List[int]) -> int:
        """
        链接:https://leetcode.cn/problems/minimum-sum-of-values-by-dividing-array/

        描述:
        给你两个数组 nums 和 andValues，长度分别为 n 和 m。
        数组的 值 等于该数组的 最后一个 元素。
        你需要将 nums 划分为 m 个 不相交的连续 子数组，对于第 ith 个子数组 [li, ri]，子数组元素的按位AND运算结果等于 andValues[i]，换句话说，对所有的 1 <= i <= m，nums[li] & nums[li + 1] & ... & nums[ri] == andValues[i] ，其中 & 表示按位AND运算符。
        返回将 nums 划分为 m 个子数组所能得到的可能的 最小 子数组 值 之和。如果无法完成这样的划分，则返回 -1 。

        示例:
        输入： nums = [1,4,3,3,2], andValues = [0,3,3,2]
        输出： 12
        解释：
        唯一可能的划分方法为：
        [1,4] 因为 1 & 4 == 0
        [3] 因为单元素子数组的按位 AND 结果就是该元素本身
        [3] 因为单元素子数组的按位 AND 结果就是该元素本身
        [2] 因为单元素子数组的按位 AND 结果就是该元素本身
        这些子数组的值之和为 4 + 3 + 3 + 2 = 12

        数据范围:
        1 <= n == nums.length <= 10^4
        1 <= m == andValues.length <= min(n, 10)
        1 <= nums[i] < 10^5
        0 <= andValues[j] < 10^5
        """
        n, m = len(nums), len(andValues)

        # 分析以下时间复杂度 i < 10 ^ 4, j < 10
        # 每次到i位置时候最多有log(nums[i])种与运算结果
        # 所以整体时间复杂度为n * m * log(U) U为nums中的最大值
        # 记住一个要点 当前的&运算结果只会越来越小
        # 所以一个数组的子数组能够产生的与运算结果只有nlog(U)种
        # 这个也可以以每个位置结尾的子数组的与运算结果的种类数来看
        # 每个子数组一定以某一个位置上的数字结尾 由于与运算的性质 最后与上位置i上的结果最多只有log(nums[i])种 
        @lru_cache(None)
        def dfs(i, pre, j):
            if i == n:
                return 0 if j == m else inf
            if j == m:
                return 0 if i == n else inf
            cur = pre & nums[i]  # 当前的&运算结果
            res = dfs(i + 1, cur, j)
            if pre < andValues[j]:
                # pre已经小于andValues[j]了 那么接着往后进行&运算只会越来越小
                # 永远不可能等于andValues[j]了 也就是一个非法的方案 所以直接返回无穷大
                return inf
            if cur == andValues[j]:
                # 如果此时进行&运算的结果等于andValues[j] 那么就可以选择这个位置
                # j往后移动一个下标
                tmp = dfs(i + 1, (1 << 30) - 1, j + 1) + nums[i]
                if tmp < res:
                    res = tmp
            return res

        ans = dfs(0, (1 << 30) - 1, 0)
        dfs.cache_clear()
        return ans if ans < inf else -1
