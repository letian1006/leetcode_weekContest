from typing import List
from itertools import accumulate


"""
链接: https://leetcode.cn/problems/find-the-count-of-monotonic-pairs-ii/description/
描述: 
给你一个长度为 n 的 正 整数数组 nums 。

如果两个 非负 整数数组 (arr1, arr2) 满足以下条件，我们称它们是 单调 数组对：

两个数组的长度都是 n 。
arr1 是单调 非递减 的，换句话说 arr1[0] <= arr1[1] <= ... <= arr1[n - 1] 。
arr2 是单调 非递增 的，换句话说 arr2[0] >= arr2[1] >= ... >= arr2[n - 1] 。
对于所有的 0 <= i <= n - 1 都有 arr1[i] + arr2[i] == nums[i] 。
请你返回所有 单调 数组对的数目。

由于答案可能很大，请你将它对 10^9 + 7 取余 后返回。

提示:
1 <= n == nums.length <= 2000
1 <= nums[i] <= 1000
"""

MOD = 10 ** 9 + 7
class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        n = len(nums)
        m = max(nums)
        # arr1[i]为j能够有多少答案为f数组的定义
        f = [[0] * (m + 1) for _ in range(n)]
        for j in range(nums[0] + 1):
            f[0][j] = 1
        for i in range(1, n):
            # j > arr1[i]
            s = list(accumulate(f[i - 1]))
            for j in range(nums[i] + 1):
                # 当前位置是j 需要枚举前面arr1[i-1]哪些数字是合法的
                # 设arr1[i-1]等于k 则 k <= j 且(nums[i-1] - k) >= (nums[i] - j)
                # 整理得到 k <= max(j, nums[i] - nums[i-1] + j) 即 k <= j + min(nums[i-1] - nums[i], 0)
                max_k = j + min(nums[i-1] - nums[i], 0)
                f[i][j] = s[max_k] % MOD if max_k >= 0 else 0
        # 返回最后一行的和 arr1的最后一个数字的取值最多到nums[-1] 因此求和的时候只需要到nums[-1]即可
        return sum(f[-1][:nums[-1] + 1]) % MOD