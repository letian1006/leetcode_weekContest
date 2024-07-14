"""
七月十四号的周赛 没有做出第四题 该题为贪心题目
"""
from typing import List


class Solution:
    def minimumCost(self, m: int, n: int, horizontalCut: List[int], verticalCut: List[int]) -> int:
        """
        链接: https://leetcode.cn/problems/minimum-cost-for-cutting-cake-ii/
        描述:
        有一个 m x n 大小的矩形蛋糕，需要切成 1 x 1 的小块。
        给你整数 m ，n 和两个数组：
        horizontalCut 的大小为 m - 1 ，其中 horizontalCut[i] 表示沿着水平线 i 切蛋糕的开销。
        verticalCut 的大小为 n - 1 ，其中 verticalCut[j] 表示沿着垂直线 j 切蛋糕的开销。
        一次操作中，你可以选择任意不是 1 x 1 大小的矩形蛋糕并执行以下操作之一：
        沿着水平线 i 切开蛋糕，开销为 horizontalCut[i] 。
        沿着垂直线 j 切开蛋糕，开销为 verticalCut[j] 。
        每次操作后，这块蛋糕都被切成两个独立的小蛋糕。
        每次操作的开销都为最开始对应切割线的开销，并且不会改变。
        请你返回将蛋糕全部切成 1 x 1 的蛋糕块的 最小 总开销。
        示例:
        输入：m = 3, n = 2, horizontalCut = [1,3], verticalCut = [5]
        输出：13
        解释：
            沿着垂直线 0 切开蛋糕，开销为 5 。
            沿着水平线 0 切开 3 x 1 的蛋糕块，开销为 1 。
            沿着水平线 0 切开 3 x 1 的蛋糕块，开销为 1 。
            沿着水平线 1 切开 2 x 1 的蛋糕块，开销为 3 。
            沿着水平线 1 切开 2 x 1 的蛋糕块，开销为 3 。
            总开销为 5 + 1 + 1 + 3 + 3 = 13 。
        """
        # 谁大先切谁 然后切割的代价就是
        # 如果这次是横切 那么就是横切的代价乘以之前竖切的次数 + 1
        # 如果是竖切 那么就是此时竖切的代价乘以之前横切的次数 + 1
        horizontalCut.sort(reverse=True)
        verticalCut.sort(reverse=True)
        ans = i = j = 0
        cnt_h = cnt_v = 1

        while i < m - 1 or j < n - 1:
            if j == n - 1 or i < m - 1 and horizontalCut[i] > verticalCut[j]:
                # 横着切一刀
                ans += horizontalCut[i] * cnt_v
                i += 1
                cnt_h += 1
            else:
                ans += verticalCut[j] * cnt_h
                j += 1
                cnt_v += 1
        return ans