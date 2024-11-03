from functools import cache
from math import gcd
from typing import List


MOD = 10 ** 9 + 7

class Solution:
    """
    链接: https://leetcode.cn/problems/find-the-number-of-subsequences-with-equal-gcd/description/
    描述: 
    给你一个整数数组 nums。请你统计所有满足一下条件的 非空 子序列对 (seq1, seq2) 的数量：
    子序列 seq1 和 seq2 不相交，意味着 nums 中 不存在 同时出现在两个序列中的下标。
    seq1 元素的 GCD等于 seq2 元素的 GCD。
    返回满足条件的子序列对的总数。由于答案可能非常大，请将它对 10^9 + 7 取余后返回。
    提示:
    1 <= nums.length <= 200
    1 <= nums[i] <= 200
    """
    def subsequencePairCount(self, nums: List[int]) -> int:
        n = len(nums)


        @cache
        def dfs(index, cur1, cur2):
            if index == n:
                return cur1 == cur2
            # 看数据范围猜算法
            # 三次方的一个东西 考虑当前数字放在哪一个集合中
            res = dfs(index + 1, cur1, cur2)
            res += dfs(index + 1, gcd(cur1, nums[index]), cur2)
            res += dfs(index + 1, cur1, gcd(cur2, nums[index]))
            res %= MOD
            return res

        ans = (dfs(0, 0, 0) - 1) % MOD  # 减去1 是代表两个集合都是空的情况了
        dfs.cache_clear()
        return ans        