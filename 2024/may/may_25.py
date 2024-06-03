"""
131场双周赛 三题目选手
第四题是一个线段树维护巧妙信息的题目
"""
from typing import List

from sortedcontainers import SortedList

MX = 10 ** 4 * 5 + 1


class Solution:
    """
    链接: https://leetcode.cn/problems/block-placement-queries/description/
    描述:
    有一条无限长的数轴，原点在 0 处，沿着 x 轴 正 方向无限延伸。
    给你一个二维数组 queries ，它包含两种操作：
    操作类型 1 ：queries[i] = [1, x] 。在距离原点 x 处建一个障碍物。数据保证当操作执行的时候，位置 x 处 没有 任何障碍物。
    操作类型 2 ：queries[i] = [2, x, sz] 。判断在数轴范围 [0, x] 内是否可以放置一个长度为 sz 的物块，这个物块需要 完全 放置在范围 [0, x] 内。
    如果物块与任何障碍物有重合，那么这个物块 不能 被放置，但物块可以与障碍物刚好接触。注意，你只是进行查询，并 不是 真的放置这个物块。每个查询都是相互独立的。
    请你返回一个 boolean 数组results ，如果第 i 个操作类型 2 的操作你可以放置物块，那么 results[i] 为 true ，否则为 false 。
    示例:
    输入：queries = [[1,7],[2,7,6],[1,2],[2,7,5],[2,7,6]]
    输出：[true,true,false]
    解释：
    查询 0 在 x = 7 处放置一个障碍物。在 x = 7 之前任何大小不超过 7 的物块都可以被放置。
    查询 2 在 x = 2 处放置一个障碍物。现在，在 x = 7 之前任何大小不超过 5 的物块可以被放置，x = 2 之前任何大小不超过 2 的物块可以被放置。
    """

    def getResults(self, queries: List[List[int]]) -> List[bool]:
        ans = []
        sl = SortedList()  # 有序表
        sl.add(0)
        tree = [0] * (MX << 2)  # 线段树 这里是维护以每个位置为结尾最长的连续空白区间

        def modify(o, l, r, index, val):
            if l == r:
                tree[o] = val
                return
            m = l + r >> 1
            if index <= m:
                modify(o << 1, l, m, index, val)
            else:
                modify(o << 1 | 1, m + 1, r, index, val)
            tree[o] = max(tree[o << 1], tree[o << 1 | 1])

        def get(o, l, r, L, R):
            if L <= l and r <= R:
                return tree[o]
            # 最长连续空白区间是多少
            m = l + r >> 1
            res = 0
            # 返回一段区间内的最大值
            if L <= m:
                res = max(res, get(o << 1, l, m, L, R))
            if R > m:
                res = max(res, get(o << 1 | 1, m + 1, r, L, R))
            return res

        for q in queries:
            if len(q) == 2:
                _, x = q  # 建造一个建筑物
                l = sl.bisect_left(x)
                left = sl[l - 1]  # 最靠左边的第一个数字是多少
                modify(1, 0, MX - 1, x, x - left)  # x位置修改为x-left
                if l != len(sl):
                    # 如果x位置右边还有障碍物
                    # 那么这个位置的障碍物代表的最大空白长度就要修改为sl[l] - x
                    right = sl[l]
                    modify(1, 0, MX - 1, right, right - x)
                sl.add(x)
            else:
                _, x, size = q
                cur = get(1, 0, MX - 1, 0, x)  # 查询区间最大值
                l = sl.bisect_left(x)
                # 查询时需要两个部分 第一个是x位置左边的最大空白长度 第二个是x位置右边的最大空白长度
                # 看看这两段长度能不能构成size长度的空白区间 如果可以就返回True 能够将size大小的物块放置进去
                ans.append(max(cur, x - sl[l - 1]) >= size)
        return ans
