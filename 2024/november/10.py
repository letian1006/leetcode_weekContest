from collections import defaultdict
from typing import List


MOD = 10 ** 9 + 7
class Solution:
    # https://leetcode.cn/problems/sum-of-good-subsequences/
    def sumOfGoodSubsequences(self, nums: List[int]) -> int:
        # 考虑每一个元素带来的收益
        # 以i结尾的子序列有多少个 has[x] + has[x-1] + has[x] + 1
        # 以i结尾的子序列的和有多少 sm[x-1] + x * has[x-1] + sm[x+1] + x * has[x+1] + sm[x] + has[x] * x + x
        has = defaultdict(int)  # 以i结尾的子序列有多少个
        sm = defaultdict(int) # 以i结尾的子序列的和有多少
        for x in nums:
            c = has[x-1] + has[x+1] + 1
            sm[x] = (sm[x-1] + has[x-1] * x +  sm[x+1] + has[x+1] * x + sm[x] + x)% MOD
            has[x] = (c + has[x]) % MOD
        
        return sum(sm.values()) % MOD

        