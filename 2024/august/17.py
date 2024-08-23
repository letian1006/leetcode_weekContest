from typing import List
from math import inf

"""

链接: https://leetcode.cn/problems/maximum-value-sum-by-placing-three-rooks-ii/
描述:
给你一个 m x n 的二维整数数组 board ，它表示一个国际象棋棋盘，其中 board[i][j] 表示格子 (i, j) 的 价值 。
处于 同一行 或者 同一列 车会互相 攻击 。你需要在棋盘上放三个车，确保它们两两之间都 无法互相攻击 。
请你返回满足上述条件下，三个车所在格子 值 之和 最大 为多少。
提示:
3 <= m == board.length <= 500
3 <= n == board[i].length <= 500
-109 <= board[i][j] <= 109
"""

class Solution:
    def maximumValueSum(self, board: List[List[int]]) -> int:

        def update(row):
            for j, x in enumerate(row):
                for k in range(3):
                    # 最大 第二大 第三大的数字以及所在的列 不能在同一列上面
                    # 记住我们维护的是不同列的前三大的数字
                    # 如果比最大的数字更大 直接替换最大值即可
                    # 如果没有比最大的数字大 但是大于第二个数字 能不能替换还要看第一个数字的脸色 你不能和他同列
                    # 最后一个数字是同理 如果你没有仅仅比第三个数字大 那么能不能更新 要看前两个数字的脸色 你不能和他们同列
                    if x > p[k][0] and all(j != j2 for _, j2 in p[:k]):
                        p[k], (x, j) = (x, j), p[k]
            
        

        # 前后缀分解加计算前缀的不同列前3大值和后缀的前3大值
        m, n = len(board), len(board[0])
        suf = [None] * m
        p = [(-inf, -1)] * 3
        for i in range(m - 1, 1, -1):
            update(board[i])
            suf[i] = p[:]  # 从后往前遍历得到后缀的不同列的第一大 第二大 第三大的数字以及所在的列
        
        ans = -inf
        p = [(-inf, -1)] * 3
        for i, row in enumerate(board[:-2]):
            update(row)
            for j2, y in enumerate(board[i+1]):
                for x, j1 in p:
                    for z, j3 in suf[i + 2]:
                        if j2 != j1 and j2 != j3 and j1 != j3:
                            # 我们是按照顺序枚举的 如果找到了第一个完全不同列的可以直接break 因为你咋suf中枚举后面的数字只会比此时枚举到的z更小
                            ans = max(ans, x + y + z)
                            break
        return ans