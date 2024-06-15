"""
链接：https://leetcode.cn/problems/find-the-maximum-length-of-a-good-subsequence-ii/
描述：
给你一个整数数组 nums 和一个 非负 整数 k 。如果一个整数序列 seq 满足在范围下标范围 [0, seq.length - 2] 中存在 不超过 k 个下标 i 满足 seq[i] != seq[i + 1] ，那么我们称这个整数序列为 好 序列。
请你返回 nums 中 好 子序列的最长长度
示例：
输入：nums = [1,2,1,1,3], k = 2
输出：4
解释：
最长好子序列为 [1,2,1,1,3] 。
"""

class Solution:
    def maximumLength(self, nums: List[int], k: int) -> int:
        # 看值域 定义f[x][j] 为x结尾的 至多j个不同的下标对的最长子序列长度
        fs = {}
        mx = [0] * (k + 2)  # mx[i]表示之前枚举的过程中 不超过i个下标对的最长子序列长度
        def max(a, b):
            return a if a > b else b
        for x in nums:
            if x not in fs:  # 如果x之前没有出现在哈希表中 记录这个值对应的f[x] 此时f[x]表示的就是以x结尾的 有至多j个不同下标对的dp数组
                fs[x] = [0] * (k + 1)
            f = fs[x]
            for j in range(k, -1, -1):  # 倒着枚举 保证使用的mx[j-1]是上一轮迭代完成的mx
                f[j] += 1  # 选中当前数字 以x结尾的j个不同的下标直接加上1
                f[j] = max(f[j], mx[j-1] + 1)  # 之前最多j-1个不同下标对的最长子序列的长度
                mx[j] = max(mx[j], f[j])
        return mx[k]
