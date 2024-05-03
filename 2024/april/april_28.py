"""
2024年4月28日的周赛题目
链接: https://leetcode.cn/contest/weekly-contest-395/
没有参加 给出第三题和第四题的代码 第三题位运算 第四题两个套路的结合
"""
from collections import Counter
from typing import List


class Solution:
    """
    链接: https://leetcode.cn/problems/minimum-array-end/description/

    描述:
    给你两个整数 n 和 x 。你需要构造一个长度为 n 的 正整数 数组 nums ，
    对于所有 0 <= i < n - 1 ，满足 nums[i + 1] 大于 nums[i] ，并且数组 nums 中所有元素的按位 AND 运算结果为 x 。
    返回 nums[n - 1] 可能的 最小 值。

    示例:
    输入：n = 3, x = 4
    输出：6
    解释：
    数组 nums 可以是 [4,5,6] ，最后一个元素为 6 。
    """

    def minEnd(self, n: int, x: int) -> int:
        """
        位运算应用 数组中的每个数一定都大于等于x 因为要求的是按位与的结果为x
        因此我们需要构造一个数组 使得数组中的每个数都大于等于x 同时使得最后一个数字最小
        所以我们就将(n-1)的二进制表示插入到x的0位置中中 以此不断增大数字的值 最后也能够得到数组的最小值
        """
        n -= 1
        i = j = 0
        while n >> j:
            # 将n的二进制表示插入到x的0位置中
            if (x >> i) & 1 == 0:
                # 只有当x的第i位是0的时候才会插入n的第j位
                x |= ((n >> j) & 1) << i
                j += 1
            i += 1
        return x

    """
    链接: https://leetcode.cn/problems/find-the-median-of-the-uniqueness-array/description/
    描述: 
    给你一个整数数组 nums 。数组 nums 的 唯一性数组 是一个按元素从小到大排序的数组，包含了 nums 的所有非空子数组中不同元素的个数。
    换句话说，这是由所有 0 <= i <= j < nums.length 的 distinct(nums[i..j]) 组成的递增数组。
    其中，distinct(nums[i..j]) 表示从下标 i 到下标 j 的子数组中不同元素的数量。
    返回 nums 唯一性数组 的 中位数 。
    注意，数组的 中位数 定义为有序数组的中间元素。如果有两个中间元素，则取值较小的那个。
    
    示例:
    输入：nums = [1,2,3]
    输出：1
    解释：
    nums 的唯一性数组为 [distinct(nums[0..0]), distinct(nums[1..1]), distinct(nums[2..2]), 
    distinct(nums[0..1]), distinct(nums[1..2]), distinct(nums[0..2])]，
    即 [1, 1, 1, 2, 2, 3] 。唯一性数组的中位数为 1 ，因此答案是 1 。

    """

    class Solution:
        def medianOfUniquenessArray(self, nums: List[int]) -> int:
            # 中位数 即第k大的数字 因此我们可以想到使用二分查找
            # 其次是我么需要知道check函数如何去写
            n = len(nums)
            al = n * (n + 1) // 2
            # 中位数 第k小的数字
            k = (al - 1) // 2 + 1

            l, r = 0, len(set(nums))
            ans = -1

            def check(num):
                # 独特元素小于num的子数组有多少个

                left = right = 0
                cnt = Counter()
                res = 0  # 记录满足条件的子数组个数
                while right < n:
                    cnt[nums[right]] += 1
                    while len(cnt) > num:
                        cnt[nums[left]] -= 1
                        if cnt[nums[left]] == 0:
                            del cnt[nums[left]]
                        left += 1
                    res += right - left + 1
                    right += 1
                return res

            while l <= r:
                mid = l + r >> 1
                if check(mid) >= k:
                    ans = mid
                    r = mid - 1
                else:
                    l = mid + 1

            return ans
