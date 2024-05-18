"""
周赛两题选手 但是创造新的高分 现在给出两个题目的代码
最重要启示就是状态压缩dp的一种套路 前面填写的数字的状态 以及之前的一个数字作为dp的参数
"""
from functools import lru_cache
from typing import List

class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        """
        链接: https://leetcode.cn/problems/maximum-difference-score-in-a-grid/description/

        描述:
        给你一个由 正整数 组成、大小为 m x n 的矩阵 grid。你可以从矩阵中的任一单元格移动到另一个位于正下方或正右侧的任意单元格（不必相邻）。从值为 c1 的单元格移动到值为 c2 的单元格的得分为 c2 - c1 。
        你可以从 任一 单元格开始，并且必须至少移动一次。
        返回你能得到的 最大 总得分。

        示例:
        输入: grid = [[9,5,7,3],[8,9,6,1],[6,7,14,3],[2,5,3,1]]
        输出: 9

        解释:
        从单元格 (0, 1) 开始，并执行以下移动：
        - 从单元格 (0, 1) 移动到 (2, 1)，得分为 7 - 5 = 2 。
        - 从单元格 (2, 1) 移动到 (2, 2)，得分为 14 - 7 = 7 。
        总得分为 2 + 7 = 9 
        """
        # 解答 用海拔的思维来思考这个问题 其实就是一个脑筋急转弯问题 
        # 我们枚举每一个点作为最后的终点 运用二维前缀和的思维找到以[i][j]为右下角的子矩阵的最小值
        # 我们就用这个作为起点 然后就可以知道以当前点为终点的最大差值 枚举每一个点就可以得到答案
        m, n = len(grid), len(grid[0])
        pre_mi = [[0x3f3f3f3f] * (n + 1) for _ in range(m + 1)]
        ans = -0x3f3f3f3f
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cur = min(pre_mi[i - 1][j], pre_mi[i][j - 1])  # 以[i][j]为右下角的子矩阵的最小值
                ans = max(ans, grid[i - 1][j - 1] - cur)  # 更新答案
                pre_mi[i][j] = min(cur, grid[i - 1][j - 1])
        return ans

    """
    链接: https://leetcode.cn/problems/find-the-minimum-cost-array-permutation/

    描述: 
    给你一个数组 nums ，它是 [0, 1, 2, ..., n - 1] 的一个排列 。对于任意一个 [0, 1, 2, ..., n - 1] 的排列 perm ，
    其 分数 定义为：score(perm) = |perm[0] - nums[perm[1]]| + |perm[1] - nums[perm[2]]| + ... + |perm[n - 1] - nums[perm[0]]|
    返回具有 最低 分数的排列 perm 。如果存在多个满足题意且分数相等的排列，则返回其中字典序最小的一个。

    示例:
    输入: nums = [1,0,2]
    输出: 输出：[0,1,2]
    解释：数组 perm = [0,1,2] 是一个符合题目要求的排列，其分数为 |0 - 1| + |1 - 0| + |2 - 2| = 2 。 是所有排列中分数最低的一个。
    """

    # 这个题目是一个状态压缩的dp题目 但是状态定义有一个套路 根据题目要求 我需要知道前面已经有哪些数字被选择了 
    # 并且我需要知道前面一个数字是谁 因此我们定义一个参数表示状压的state 一个参数表示前面一个数字是谁
    # 最后需要注意的是这个题目的答案第一个数字必定是0 假设[1, 2, 3, 0]是符合要求的最短数组 那么他的每一个循环数组都可以得到最小分数
    # 因为score(perm) = |perm[0] - nums[perm[1]]| + |perm[1] - nums[perm[2]]| + ... + |perm[n - 1] - nums[perm[0]]| 这个就说明了
    # 这个数组的循环数组得分都是一样的 题目要求的是字典序最小的一个 所以第一个数字必定是0
    def findPermutation(self, nums: List[int]) -> List[int]:

        n = len(nums)
        al = (1 << n) - 1
        @lru_cache(None)
        def dfs(state, pre):
            if state == al:
                return abs(pre - nums[0]) # 所有数字填完 返回最后一个数字和nums[0]的差值的绝对值 也就是最后一项|perm[n - 1] - nums[perm[0]]|
            res = 0x3f3f3f3f
            for i in range(1, n):
                if (state >> i) & 1 == 0:
                    res = min(res, abs(pre - nums[i]) + dfs(state | (1 << i), i))  # 得到最小的得分
            return res

        mi_socre = dfs(1, 0)  # 从0开始填

        ans = []

        def make_ans(state, pre):
            ans.append(pre)
            if state == al:
                return
            target = dfs(state, pre) # 得到当前状态的最小得分
            # 按照dfs的记忆化搜索中的数据 一路搜索下去得到路径 填充到ans中
            for i in range(1, n):
                if (state >> i) & 1 == 0 and abs(pre - nums[i]) + dfs(state | (1 << i), i) == target:
                    make_ans(state | (1 << i), i)
                    break
        make_ans(1, 0)

        dfs.cache_clear()
        return ans
    
