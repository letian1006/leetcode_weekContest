"""
1. 2023年11月5日
参加的周赛 两题选手
第三题没有想到正难则反的思路 直接正着来很难思考
但是还是树形dp的思路 也就是选择或者不选 以及枚举选哪个的思路 这里是决定是不是损失头节点的分数来作为状态

第四题就是一个数据结构优化dp，但是最关键的不是使用树状数组或者线段树来修改或者查询某个区间的最大值
而是要注意到值域上是连续的，所以我们可以离散化，然后使用树状数组或者线段树来维护前缀最大值
横看成岭侧成峰 这就要求我们多做题累积一个敏锐的思路
"""
from bisect import bisect_left
from math import inf
from typing import List


# 单点修改 前缀最大值
class BIT:
    def __init__(self, n):
        self.data = [-inf] * n

    def update(self, i: int, val: int) -> None:
        # 修改单点最大值
        while i < len(self.data):
            self.data[i] = max(self.data[i], val)
            i += i & -i

    def query(self, i: int) -> int:
        # 查询前缀最大值
        res = -inf
        while i:
            res = max(res, self.data[i])
            i &= i - 1
        return res


class Solution:
    # https://leetcode.cn/problems/maximum-balanced-subsequence-sum/description/
    # 数据结构的优化 需要注意离散化 前缀最大值 线段树或者树状数组
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        # 数据结构优化dp 我们要做的意识到值域上是连续的 下标虽然不连续
        b = sorted(set(c - i for i, c in enumerate(nums)))  # 离散化
        tree = BIT(len(b) + 1)
        ans = -inf
        # 前缀最大值
        for i, c in enumerate(nums):
            index = bisect_left(b, c - i) + 1
            f = max(tree.query(index), 0) + c
            ans = max(ans, f)
            tree.update(index, f)
        return ans

    # https://leetcode.cn/problems/maximum-score-after-applying-operations-on-a-tree/
    def maximumScoreAfterOperations(self, edges: List[List[int]], values: List[int]) -> int:
        # 正难则反的树形dp问题
        n = len(values)
        g = [[] for _ in range(n)]
        g[0].append(-1)

        for a, b in edges:
            g[a].append(b)
            g[b].append(a)

        def dfs(x: int, fa: int) -> int:
            if len(g[x]) == 1:
                return values[x]
            loss = 0
            # 以x为头的子树是健康的 需要损失的最小值
            for nex in g[x]:
                if nex != fa:
                    loss += dfs(nex, x)
            return min(values[x], loss)

        return sum(values) - dfs(0, -1)
