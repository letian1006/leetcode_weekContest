"""
2024-1-20日的双周赛
两题选手 记得t3和t4两道题没有做出
下面给出t1和t2的代码
"""
from typing import List
from sortedcontainers import SortedList


class Solution:
    def minimumArrayLength(self, nums: List[int]) -> int:
        """
        链接:https://leetcode.cn/problems/minimize-length-of-array-using-operations/

        描述:
        给你一个下标从 0 开始的整数数组 nums ，它只包含 正 整数。
        你的任务是通过进行以下操作 任意次 （可以是 0 次） 最小化 nums 的长度：
        在 nums 中选择 两个不同 的下标 i 和 j ，满足 nums[i] > 0 且 nums[j] > 0 。
        将结果 nums[i] % nums[j] 插入 nums 的结尾。
        将 nums 中下标为 i 和 j 的元素删除。
        请你返回一个整数，它表示进行任意次操作以后 nums 的 最小长度 。

        示例:
        输入：nums = [1,4,3,1]
        输出：1
        解释：使数组长度最小的一种方法是：
        操作 1 ：选择下标 2 和 1 ，插入 nums[2] % nums[1] 到数组末尾，得到 [1,4,3,1,3] ，然后删除下标为 2 和 1 的元素。
        nums 变为 [1,1,3] 。
        操作 2 ：选择下标 1 和 2 ，插入 nums[1] % nums[2] 到数组末尾，得到 [1,1,3,1] ，然后删除下标为 1 和 2 的元素。
        nums 变为 [1,1] 。
        操作 3 ：选择下标 1 和 0 ，插入 nums[1] % nums[0] 到数组末尾，得到 [1,1,0] ，然后删除下标为 1 和 0 的元素。
        nums 变为 [0] 。
        nums 的长度无法进一步减小，所以答案为 1 。
        1 是可以得到的最小长度。
        """
        # 如果数组中最小的数只有一个 那么我们直接选择最小的数和数组中的其他数字做模运算
        # 那么相当于每次减少一个数 这样重复下去 我们最后得到的数组长度最小就是1
        # 如果数组中最小的数有多个 但是我们可以通过模运算 得到一个更小的数 那么就可以归结到上面的情形
        # 如果数组中所有的数都是最小的数的倍数，那么我们将这些较大的数字全部通过模运算将其消去
        # 最后数组中剩下的就全部是最小的数字 我们再两两配对 最后剩下的数组长度就是(cnt[min(nums)] + 1) // 2
        m = min(nums)
        cnt = 0
        for i in nums:
            if i % m != 0:
                return 1
            if i == m:
                cnt += 1
        return (cnt + 1) // 2

    def minimumCost(self, nums: List[int], k: int, dist: int) -> int:
        """
        链接:https://leetcode.cn/problems/divide-an-array-into-subarrays-with-minimum-cost-ii/description/

        描述:
        给你一个下标从 0 开始长度为 n 的整数数组 nums 和两个 正 整数 k 和 dist 。
        一个数组的 代价 是数组中的 第一个 元素。比方说，[1,2,3] 的代价为 1 ，[3,4,1] 的代价为 3 。
        你需要将 nums 分割成 k 个 连续且互不相交 的子数组，满足 第二 个子数组与第 k 个子数组中第一个元素的下标距离 不超过 dist 。
        换句话说，如果你将 nums 分割成子数组 nums[0..(i1 - 1)], nums[i1..(i2 - 1)], ..., nums[ik-1..(n - 1)] ，
        那么它需要满足 ik-1 - i1 <= dist 。
        请你返回这些子数组的 最小 总代价。

        示例:
        输入：nums = [1,3,2,6,4,2], k = 3, dist = 3
        输出：5
        解释：将数组分割成 3 个子数组的最优方案是：[1,3] ，[2,6,4] 和 [2] 。这是一个合法分割，因为 ik-1 - i1 等于 5 - 2 = 3 ，等于 dist 。总代价为 nums[0] + nums[2] + nums[5] ，也就是 1 + 2 + 2 = 5 。
        5 是分割成 3 个子数组的最小总代价
        """
        # 题目就是维护窗口大小为dist的窗口的k-1个最小值
        k -= 1
        sl = SortedList(nums[1:dist + 2])
        ans = s = sum(sl[:k])
        for i in range(dist + 2, len(nums)):
            # 加进去的元素小于第k大的元素 我们剔除第k大的元素 同时加入这个小一点的元素
            if nums[i] < sl[k - 1]:
                s += nums[i] - sl[k - 1]
            sl.add(nums[i])
            sl.remove(nums[i - dist - 1])
            # 如果踢出去的元素小于第k大的元素 那么我们剔除原来的元素 同时加入新的元素
            if nums[i - dist - 1] < sl[k - 1]:
                s += sl[k - 1] - nums[i - dist - 1]
            ans = min(ans, s)
        return ans + nums[0]
