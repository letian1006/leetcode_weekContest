"""
23年的倒数第二场周赛
3题选手 最后一题是一个弗洛伊德dp 最短路dp问题
"""
from collections import defaultdict
from functools import cache
from math import inf
from typing import List


class Solution:
    """
    链接：https://leetcode.cn/problems/minimum-cost-to-convert-string-ii/
    给你两个下标从 0 开始的字符串 source 和 target ，它们的长度均为 n 并且由 小写 英文字母组成。
    另给你两个下标从 0 开始的字符串数组 original 和 changed ，以及一个整数数组 cost ，其中 cost[i] 代表将字符串 original[i] 更改为字符串 changed[i] 的成本。
    你从字符串 source 开始。在一次操作中，如果 存在 任意 下标 j 满足 cost[j] == z  、original[j] == x 以及 changed[j] == y ，
    你就可以选择字符串中的 子串 x 并以 z 的成本将其更改为 y 。
    你可以执行 任意数量 的操作，但是任两次操作必须满足 以下两个 条件 之一 ：
    在两次操作中选择的子串分别是 source[a..b] 和 source[c..d] ，满足 b < c  或 d < a 。换句话说，两次操作中选择的下标 不相交 。
    在两次操作中选择的子串分别是 source[a..b] 和 source[c..d] ，满足 a == c 且 b == d 。换句话说，两次操作中选择的下标 相同 。
    返回将字符串 source 转换为字符串 target 所需的 最小 成本。如果不可能完成转换，则返回 -1 。
    注意，可能存在下标 i 、j 使得 original[j] == original[i] 且 changed[j] == changed[i] 。
    """

    """
    1 <= source.length == target.length <= 1000
    source、target 均由小写英文字母组成
    1 <= cost.length == original.length == changed.length <= 100
    1 <= original[i].length == changed[i].length <= source.length
    original[i]、changed[i] 均由小写英文字母组成
    original[i] != changed[i]
    1 <= cost[i] <= 106
    """
    # 解释题目的含义 也就是字符串直接是形成一个图的
    # 那两个条件给予我们的要求就是 可以根据字符串source和target当前位置的字符是不是相等
    # 来考虑dp的状态转移
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        len_to_strs = defaultdict(set)
        dis = defaultdict(lambda: defaultdict(lambda: inf))
        # 以长度划分转换连通块 长度不同的肯定是不联通的
        # 这个地方是为了降低常数 否则我们需要枚举的长度很多 会超时
        # 题目给的changed数组长度只有100 我们至多有100个不同的长度的字符串
        # 如果不做分组 单纯枚举长度 因为source字符串的长度是1000 所以再后续的dfs过程中 就会有很多长度需要没觉
        # 反之就很简单了
        for x, y, c in zip(original, changed, cost):
            len_to_strs[len(x)].add(x)
            len_to_strs[len(y)].add(y)
            dis[x][y] = min(dis[x][y], c)
            dis[x][x] = 0
            dis[y][y] = 0

        # 按照长度分组 长度相同的在一个连通块里面
        # 对这个连通块跑一个Floyd算法 计算各个字符串节点间的最短路
        # 供下面的dp使用
        for strs in len_to_strs.values():
            for k in strs:
                for i in strs:
                    for j in strs:
                        dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])

        @cache
        def dfs(i):
            if i == 0:
                return 0
            res = inf
            # 当前字符相同 可以选择不替换 这样直接跳到前一个字符 得到一个子问题
            if source[i - 1] == target[i - 1]:
                res = dfs(i - 1)
            # 以i结尾的长度
            # 枚举长度
            for size, strs in len_to_strs.items():
                # 枚举长度为size的字符串 其中strs是一个hashset
                # 这里面的字符串我们已经求过替换的最小代价了
                if i < size:
                    # 如果当前枚举的字符串长度大于i 那么就不用考虑了
                    continue
                s = source[i - size:i]
                t = target[i - size:i]
                if s in strs and t in strs:
                    res = min(res, dis[s][t] + dfs(i - size))
            return res

        ans = dfs(len(source))
        dfs.cache_clear()

        return ans if ans < inf else -1

