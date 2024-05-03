"""
2024年4月27日的双周赛 没有参加
链接: https://leetcode.cn/contest/biweekly-contest-129/
给出第三题和第四题的代码 两题的题面相同 数据范围不同
"""
from functools import cache

MOD = 10 ** 9 + 7


class Solution:
    """
    链接: https://leetcode.cn/problems/find-all-possible-stable-binary-arrays-i/submissions/528947449/
    描述:
    给你 3 个正整数 zero ，one 和 limit 。
    一个二进制数组arr 如果满足以下条件，那么我们称它是稳定的：
    0 在 arr 中出现次数 恰好 为 zero 。
    1 在 arr 中出现次数 恰好 为 one 。
    arr 中每个长度超过 limit的子数组都 同时 包含 0 和 1 。
    请你返回 稳定 二进制数组的总数目。
    由于答案可能很大，将它对 1e9 + 7 取余 后返回。
    示例:
    输入：zero = 3, one = 3, limit = 2
    输出：14
    解释：
    所有稳定的二进制数组包括 [0,0,1,0,1,1] ，[0,0,1,1,0,1] ，[0,1,0,0,1,1] ，
    [0,1,0,1,0,1] ，[0,1,0,1,1,0] ，[0,1,1,0,0,1] ，[0,1,1,0,1,0] ，
    [1,0,0,1,0,1] ，[1,0,0,1,1,0] ，[1,0,1,0,0,1] ，[1,0,1,0,1,0] ，
    [1,0,1,1,0,0] ，[1,1,0,0,1,0] 和 [1,1,0,1,0,0] 。
    """

    def numberOfStableArrays(self, zero: int, one: int, limit: int) -> int:
        """
        定义状态为使用i个0 j个1 且第i+j位置上填k的合法方案数目 为dfs(i, j, k)
        所以答案就是dfs(zero, one, 0) + dfs(zero, one, 1)
        牢牢记住这个定义的是合法方案数目 但是这个的转移方程不太好想
        假设我们现在要计算dfs(i,j,0)表示最后一位是0 的合法方案数目 那么之前一位根据填写的数字是0和1可以分为两个部分
        dfs(i-1, j, 0) + dfs(i-1, j, 1) 但是前一个位置填写0的合法方案中会出现导致不合法的整体方案出现
        即dfs(i-limit-1, j, 1)就是末尾填写limit个0的方案数目，这个方案在dfs(i-1, j, 0)中是合法的 需要减去
        所以最后的转移方程就是dfs(i-1, j, 0) + dfs(i-1, j, 1) -(dfs(i-limit-1, j, 1)
        即dfs(i,j,0) = (dfs(i-1, j, 0) + dfs(i-1, j, 1) - dfs(i-limit-1, j, 1)
        """

        @cache
        def dfs(i, j, k):
            if i == 0:
                return 1 if k == 1 and j <= limit else 0
            if j == 0:
                return 1 if k == 0 and i <= limit else 0

            if k == 0:
                return (dfs(i - 1, j, 0) + dfs(i - 1, j, 1) - (dfs(i - limit - 1, j, 1) if i > limit else 0)) % MOD
            else:
                return (dfs(i, j - 1, 0) + dfs(i, j - 1, 1) - (dfs(i, j - limit - 1, 0) if j > limit else 0)) % MOD

        ans = (dfs(zero, one, 0) + dfs(zero, one, 1)) % MOD

        dfs.cache_clear()
        return ans
