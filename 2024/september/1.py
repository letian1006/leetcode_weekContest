from typing import List
from functools import cache

class Solution:
    """
    链接: https://leetcode.cn/problems/select-cells-in-grid-with-maximum-score/

    描述: 
    给你一个由正整数构成的二维矩阵 grid。
    你需要从矩阵中选择 一个或多个 单元格，选中的单元格应满足以下条件：
    所选单元格中的任意两个单元格都不会处于矩阵的 同一行。
    所选单元格的值 互不相同。
    你的得分为所选单元格值的总和。
    返回你能获得的 最大 得分。

    提示:
    1 <= grid.length, grid[i].length <= 10
    1 <= grid[i][j] <= 100
    """
    def maxScore(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        # 换一个角度 从值域开始看 要从哪些行中间选数 考虑选了哪些行 而不是之前选了哪些数字 这样会产生很多状态
        # dfs(i, j)表示从1到i这个值域之间选数字 j代表之前选过的行 作为禁止状态
        # 状态太多的时候需要换一个角度 值域角度就是一个很好的思维 不要去想哪些数字选过 而是想哪些行被选了 
        mx = max(map(max, grid))
        rows = [[] for _ in range(mx + 1)]  # 这个数组是记录每个数字存在于哪些行 供后面dfs到i时候 枚举选择哪一行使用的
        for i, row in enumerate(grid):
            for num in set(row): # 去重 
                rows[num].append(i)
        # return ans
        @cache
        def dfs(i, j):
            if i == 0:
                return 0
            res = dfs(i - 1, j)
            for row in rows[i]:
                # 当前数字是i 我要选那一行作为承载这个数字的行
                if j >> row & 1 == 0:  # 这一行之前不能被选过
                    res = max(res, dfs(i - 1, j | (1 << row)) + i)
            return res


        ans = dfs(mx, 0)
        dfs.cache_clear()
        return ans


    """
    链接: https://leetcode.cn/problems/maximum-xor-score-subarray-queries/description/

    描述: 
    给你一个由 n 个整数组成的数组 nums，以及一个大小为 q 的二维整数数组 queries，其中 queries[i] = [li, ri]。
    对于每一个查询，你需要找出 nums[li..ri] 中任意 子数组的 最大异或值。
    数组的异或值 需要对数组 a 反复执行以下操作，直到只剩一个元素，剩下的那个元素就是 异或值：
    对于除最后一个下标以外的所有下标 i，同时将 a[i] 替换为 a[i] XOR a[i + 1] 。
    移除数组的最后一个元素。
    返回一个大小为 q 的数组 answer，其中 answer[i] 表示查询 i 的答案。

    提示:
    1 <= n == nums.length <= 2000
    0 <= nums[i] <= 2^31 - 1
    1 <= q == queries.length <= 10^5
    queries[i].length == 2
    queries[i] = [li, ri]
    0 <= li <= ri <= n - 1
    """
    def maximumSubarrayXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        # 区间dp套区间dp的题目
        # 首先设f[i][j] 表示[i-j]这段数组的数组异或值 mx[i][j] 表示这段数组的任意子数组最大异或值
        # 我们通过观察可以知道f[i][j] = f[i][j-1] ^ f[i+1][j] 记住在手玩小例子的时候不要忽略过程 某些过程会给你很大的启发
        # 至于mx[i][j] 就可以分成三个部分 max(f[i][j](整个数组), mx[i][j-1](不取右端点), mx[i+1][j](不取左端点)) 经典的分类套路求区间最大值
        n = len(nums)
        f = [[0] * n for _ in range(n)]
        mx = [[0] * n for _ in range(n)]

        # 按照状态转移图 先从下到上 再从左到右
        for i in range(n - 1, -1, -1):
            mx[i][i] = f[i][i] = nums[i]
            for j in range(i + 1, n):
                f[i][j] = f[i][j-1] ^ f[i+1][j]
                mx[i][j] = max(f[i][j], mx[i][j-1], mx[i+1][j])
        return [mx[l][r] for l, r in queries]
