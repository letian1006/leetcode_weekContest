from collections import Counter
from functools import cache
from math import gcd
from typing import List


MOD = 10 ** 9 + 7


def mm(m1, m2):
    n = len(m1)
    m = len(m2[0])
    # 返回两个矩阵的乘积
    res = [[0] * m for _ in range(n)]
    tmp = list(zip(*m2))
    for i in range(n):
        for j in range(m):
            res[i][j] = sum(x * y for x, y in zip(m1[i], tmp[j]))
            res[i][j] %= MOD
    return res


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
    
    """
    矩阵快速幂 的计算 得到答案
    链接: https://leetcode.cn/problems/total-characters-in-string-after-transformations-ii/
    描述: 
    给你一个由小写英文字母组成的字符串 s，一个整数 t 表示要执行的 转换 次数，以及一个长度为 26 的数组 nums。每次 转换 需要根据以下规则替换字符串 s 中的每个字符：
    将 s[i] 替换为字母表中后续的 nums[s[i] - 'a'] 个连续字符。例如，如果 s[i] = 'a' 且 nums[0] = 3，则字符 'a' 转换为它后面的 3 个连续字符，结果为 "bcd"。
    如果转换超过了 'z'，则 回绕 到字母表的开头。例如，如果 s[i] = 'y' 且 nums[24] = 3，则字符 'y' 转换为它后面的 3 个连续字符，结果为 "zab"。
    返回 恰好 执行 t 次转换后得到的字符串的 长度。
    """
    def get(self, x, e):
        # 输出x ^ a的答案 类似于爬楼梯 乌龟生兔子 兔子生乌龟之类的题目
        cur = x
        res = [[1] for _ in range(26)]  # 单位列向量

        while e:
            if e & 1:
                # 此时有快速幂上的标志位
                res = mm(cur, res)
            cur = mm(cur, cur)
            e >>= 1
        return res


    def lengthAfterTransformations(self, s: str, t: int, nums: List[int]) -> int:
        matrix = [[0] * 26 for _ in range(26)]

        # 初始化系数矩阵
        for i, c in enumerate(nums):
            # 每个字母会造成哪些影响 类似于一个兔子会生出那些不同种类的兔子
            cur = matrix[i]
            for j in range(1, c + 1):
                cur[(j + i) % 26] += 1
        
        ele = self.get(matrix, t)
        ans = 0
        for k, v in Counter(s).items():
            ans += ele[ord(k) - ord('a')][0] * v
        return ans % MOD
    


